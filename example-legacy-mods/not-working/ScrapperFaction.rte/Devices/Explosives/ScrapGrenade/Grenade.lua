function Create(self)

	self.effectiveDistance = 120;
	self.dropoffDistance = self.effectiveDistance * 0.416
	self.num2 = -1;
	self.random = math.random(1500);
	
	--self.lifeTimer = Timer();
	self.activated = false;
	self.payloadActive = false;
	self.sfxPlayed = false;

end

function Update(self)

	if self:IsActivated() and self.activated == false then
	
		--self.lifeTimer:Reset();
		self.activated = true;

	end	
	
	--if self.activated == true and self.lifeTimer:IsPastSimMS(2500+self.random) and self.sfxPlayed == false then
	
	if self.Fuze then
		if self.activated == true and self.Fuze:IsPastSimMS(2500+self.random) and self.sfxPlayed == false then
			local Payload = CreateMOSRotating("Scrap Grenade Payload", "ScrapperFaction.rte")
			if Payload then
				Payload.Pos = self.Pos
				MovableMan:AddParticle(Payload)
				Payload:GibThis()
				self.payloadActive = true;
			end
			
			local sfx = CreateAEmitter("Explosion Nose Medium");
			sfx.Pos = self.Pos;
			MovableMan:AddParticle(sfx);	
		
			self.sfxPlayed = true;
			
			self:GibThis()
		end
	elseif self:IsActivated() then
		self.Fuze = Timer()

	end
end

function Destroy(self)

	if ActivityMan:ActivityRunning() and self.payloadActive == true then -- for some reason the game crashes if you switch activities (i.e. start a new one) while this item is active
										  -- presumably it attempts to destroy this, which then tells it to spawn a buncha stuff and it just goes mad
										  -- this check is to see if the activity is running, since you have to be paused to switch activities. hopefully.
										  -- it is possible Void Wanderers switches activities without pausing. thus this may not work and induce a crash

		local Vector2 = Vector(0,-700);

		local Vector2Left = Vector(0,-700):RadRotate(45);

		local Vector2Right = Vector(0,-700):RadRotate(-45);

		local Vector3 = Vector(0,0);

		local Vector4 = Vector(0,0);

		self.ray = SceneMan:CastObstacleRay(self.Pos, Vector2, Vector3, Vector4, self.RootID, self.Team, 128, 7);

		self.rayRight = SceneMan:CastObstacleRay(self.Pos, Vector2Right, Vector3, Vector4, self.RootID, self.Team, 128, 7);

		self.rayLeft = SceneMan:CastObstacleRay(self.Pos, Vector2Left, Vector3, Vector4, self.RootID, self.Team, 128, 7);
		
		if self.ray < 0 or self.rayRight < 0 or self.rayLeft < 0 then	
		
			local sfx = CreateAEmitter("Explosion Reflection");
			sfx.Pos = self.Pos;
			MovableMan:AddParticle(sfx);		
		
		else
			
			if self.ray > 200 or self.rayRight > 200 or self.rayLeft > 200 then
			
				local sfx = CreateAEmitter("Explosion Reflection Big Indoors");
				sfx.Pos = self.Pos;
				MovableMan:AddParticle(sfx);	
				
			else
			
				local sfx = CreateAEmitter("Explosion Reflection Indoors");
				sfx.Pos = self.Pos;
				MovableMan:AddParticle(sfx);	
				
			end
		end	

		local sfx = CreateAEmitter("Explosion Add Small");
		sfx.Pos = self.Pos;
		MovableMan:AddParticle(sfx);	

		local sfx = CreateAEmitter("Explosion CoreBass Small");
		sfx.Pos = self.Pos;
		MovableMan:AddParticle(sfx);	

		local sfx = CreateAEmitter("Explosion Ambience Small");
		sfx.Pos = self.Pos;
		MovableMan:AddParticle(sfx);	

		for actor in MovableMan.Actors do
			if actor.Team ~= self.Team then -- doesn't actually discriminate, grenade has no team
				local d = SceneMan:ShortestDistance(actor.Pos, self.Pos, true).Magnitude;
				if d < self.effectiveDistance then
					local strength = SceneMan:CastStrengthSumRay(self.Pos, actor.Pos, 0, 128);
					if strength < 500 then
						if d > self.dropoffDistance then
							actor.Health = actor.Health - (35*150*self.dropoffDistance/(actor.Mass*1)/d); -- might accidentally take in weapon weight?
						else
							actor.Health = actor.Health - (35*150/(actor.Mass*1));
						end
						if actor.Health <= 0 then
							local vector = (actor.Pos - self.Pos); -- get the actor position relative to nade, hopefully
							actor.Vel = actor.Vel + (vector / (vector.Magnitude*0.3)); -- add velocity awaywards, divide by magnitude so farther away = less vel
							self.num = math.abs(vector.Y) - math.abs(vector.X);
							if self.num < 1 then
								self.num = 1;
							end
							actor.Status = 1;
							if vector.X < 0 then
								self.num2 = 1;
							end
							actor.AngularVel = (actor.AngularVel + (35 / self.num / (vector.Magnitude*0.6))) * self.num2;
						end
					else
						if IsAHuman(actor) then -- if it is a human check for head
							local strength = SceneMan:CastStrengthSumRay(self.Pos, ToAHuman(actor).Head.Pos, 0, 128);	
							if strength < 500 then		
								if d > self.dropoffDistance then
									actor.Health = actor.Health - (35*150*self.dropoffDistance/(actor.Mass*1)/d); -- might accidentally take in weapon weight?
								else
									actor.Health = actor.Health - (35*150/(actor.Mass*1));
								end	
							end
						end
					end
				end
			end
		end
	end
end