function Create(self)

	self.actionPhase = 0;
	self.stuck = false;

end

function Update(self)

	local actor
	local parent
	actor = MovableMan:GetMOFromID(self.RootID);
	if actor and IsAHuman(actor) then
		parent = ToAHuman(actor);
		self.Team = parent.Team;
	end

	if math.random() < 0.02 then
		part = CreateMOSParticle("Flame Smoke 1");
		part.Pos = self.Pos+Vector(2*math.random(),0):RadRotate(math.random()*(math.pi*2));
		part.Vel = (self.Vel*math.random())+Vector(0,-5)+Vector(math.random()*1,0):RadRotate(math.random()*(math.pi*2));
		part.Lifetime = part.Lifetime * RangeRand(0.2,0.3);
		MovableMan:AddParticle(part);

		if math.random() < 0.5 then
			part = CreateMOPixel("Ground Fire Burn Particle");
			part.Pos = self.Pos+Vector(math.random(),0):RadRotate(math.random()*(math.pi*2));
			part.Vel = (self.Vel*math.random())+Vector(0,-10)+Vector(math.random()*5,0):RadRotate(math.random()*(math.pi*2));
			MovableMan:AddParticle(part);
		end

	elseif math.random() < 0.04 then
		part = CreateMOSParticle("Small Smoke Ball 1");--
		part.Pos = self.Pos+Vector(2*math.random(),0):RadRotate(math.random()*(math.pi*2));
		part.Vel = (self.Vel*math.random())+Vector(0,-4)+Vector(math.random()*2,0):RadRotate(math.random()*(math.pi*2));
		part.Lifetime = part.Lifetime * RangeRand(1.0,1.5);
		MovableMan:AddParticle(part);

	elseif math.random() < 0.06 then
		part = CreateMOSParticle("Tiny Smoke Ball 1");--
		part.Pos = self.Pos+Vector(2*math.random(),0):RadRotate(math.random()*(math.pi*2));
		part.Vel = (self.Vel*math.random())+Vector(0,-3)+Vector(math.random()*3,0):RadRotate(math.random()*(math.pi*2));
		part.Lifetime = part.Lifetime * RangeRand(1.0,1.5);
		MovableMan:AddParticle(part);

	end

	if math.random() > 0.99 then
		local dist, part, chosenpart
		local curdist = 25

		--Cycle through all MOs and see which is the closest.
		for i = 1, MovableMan:GetMOIDCount() - 1 do
			part = MovableMan:GetMOFromID(i)
			if part and part.ClassName ~= "MOSParticle" and part.ClassName ~= "MOPixel" and part.ClassName ~= "HDFirearm" and part.ClassName ~= "HeldDevice" then
				part = ToMovableObject(part)
				dist = SceneMan:ShortestDistance(self.Pos, part.Pos, false).Magnitude
				if dist < curdist then
					curdist = dist
					chosenpart = part
				end
			end
		end

		--If a part was found in the range, find its parent actor and burn it.
		if chosenpart then
			local MO = MovableMan:GetMOFromID(chosenpart.RootID)
			if MovableMan:IsActor(MO) then
				MO = ToActor(MO)
				MO.Health = MO.Health - 100 / MO.Mass	-- reduce damage to heavy actors
			end
		end
	end
	
	if self.actionPhase == 0 then
		local rayHitPos = Vector(0,0);
		local rayHit = false;
		for i = 1, 15 do
			local checkPos = self.Pos + Vector(self.Vel.X,self.Vel.Y):SetMagnitude(i);
			local checkPix = SceneMan:GetMOIDPixel(checkPos.X,checkPos.Y);
			if checkPix ~= rte.NoMOID and (self.ID == rte.NoMOID or (self.ID ~= rte.NoMOID and checkPix ~= self.ID)) and MovableMan:GetMOFromID(checkPix).Team ~= self.Team then
				checkPos = checkPos + SceneMan:ShortestDistance(checkPos,self.Pos,SceneMan.SceneWrapsX):SetMagnitude(3);
				self.target = MovableMan:GetMOFromID(checkPix);
				self.stickpositionX = checkPos.X-self.target.Pos.X;
				self.stickpositionY = checkPos.Y-self.target.Pos.Y;
				self.stickrotation = self.target.RotAngle;
				self.stickdirection = self.RotAngle;
				self.stuck = true;
				rayHit = true;
				break;
			end
		end
		if rayHit == true then
			self.actionPhase = 1;
		else
			if SceneMan:CastStrengthRay(self.Pos,Vector(self.Vel.X,self.Vel.Y):SetMagnitude(15),0,rayHitPos,0,0,SceneMan.SceneWrapsX) == true then
				self.Pos = rayHitPos + SceneMan:ShortestDistance(rayHitPos,self.Pos,SceneMan.SceneWrapsX):SetMagnitude(3);
			--	self.PinStrength = 1000;
				self.AngularVel = 0;
				self.stuck = true;
				self.actionPhase = 2;
				self.HitsMOs = false;
			end
		end
	elseif self.actionPhase == 1 then
		if self.target ~= nil and self.target.ID ~= 255 then
			self.Pos = self.target.Pos + Vector(self.stickpositionX,self.stickpositionY):RadRotate(self.target.RotAngle-self.stickrotation);
			self.RotAngle = self.stickdirection+(self.target.RotAngle-self.stickrotation);
		--	self.PinStrength = 1000;
			self.Vel = Vector(0,0);
			self.HitsMOs = false;
		else
		--	self.PinStrength = 0;
			self.actionPhase = 0;
			self.HitsMOs = true;
		end
	end	
	
	
end