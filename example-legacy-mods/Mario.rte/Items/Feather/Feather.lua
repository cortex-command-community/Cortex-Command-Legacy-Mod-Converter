function Create(self)
	self.boost = 10;
	
	self.updateTimer = Timer();
	self.updateDelay = 300;	-- Time window to pickup after dropped
	
	self.sparkleTimer = Timer();
	self.sparkleDelay = 300;
	
	self.flapDelayMax = 500;
	self.flapDelay = self.flapDelayMax;
	self.flapTimer = Timer();
	
	self.frameToShow = 0;
end
function Update(self)
	self.AngularVel = self.AngularVel / 2;
	self.RotAngle = 0;
	local parent = self:GetParent();
	local target = self;
	if self.targetActor then
		self.GetsHitByMOs = false;
		self.Scale = 0;
		self.HUDVisible = false;
		self.JointStrength = -1;
		self.Vel = Vector(0, 0);
		self.Pos = Vector(0, 0);
		self.ToSettle = false;
		if IsActor(self.targetActor) and self.targetActor.Status < 3 and self.targetActor.Health > (self.targetActor.MaxHealth / 2) then
			target = self.targetActor;	-- Where to position the wings
			if self.targetActor.Head then
				target = self.targetActor.Head;
			end
			if self.flapTimer:IsPastSimMS(self.flapDelay) then
				self.flapTimer:Reset();
				if self.flapDelay < self.flapDelayMax then
					self.flapDelay = self.flapDelay * 1.2;
				else
					self.flapDelay = self.flapDelayMax;
				end
				if self.frameToShow == 0 then
					self.frameToShow = 1;
				else
					self.frameToShow = 0;
				end
			end
			local negNum = 1;
			if self.targetActor.HFlipped then
				negNum = -1;
			end
			local mass = 1 + math.sqrt(self.targetActor.Mass) * 0.1;
			local boost = self.boost / mass;
			if self.targetActor:GetController():IsState(Controller.BODY_JUMPSTART) then
				if self.targetActor.Status > 0 then	-- Point actor towards flying direction if discombobulated
					self.targetActor.AngularVel = self.targetActor.AngularVel / 2 - self.targetActor.RotAngle - 1.5 * negNum;
				else	-- Otherwise try to keep upright
					self.targetActor.AngularVel = self.targetActor.AngularVel / 2 - self.targetActor.RotAngle;
				end
				self.flapDelay = self.flapDelayMax * 0.1;
				self.targetActor:GetController():SetState(Controller.BODY_JUMPSTART, false);
				self.targetActor.Vel = self.targetActor.Vel * (1 - 0.5 / boost) + Vector(boost / 2, 0):RadRotate(self.targetActor:GetAimAngle(true)) + Vector(0, -boost);
				AudioMan:PlaySound("Mario.rte/Sounds/smw/smw_jump.wav ", SceneMan:TargetDistanceScalar(self.targetActor.Pos), false, true, -1);
			elseif not self.targetActor:GetController():IsState(Controller.BODY_CROUCH) then
				self.targetActor.Vel = self.targetActor.Vel / (1 + (self.targetActor.Vel.Magnitude / mass) * 0.002) - (SceneMan.GlobalAcc * 0.002) / mass;
				self.targetActor.AngularVel = self.targetActor.AngularVel / (1 + math.abs(self.targetActor.AngularVel / mass * 0.01));
			else
				self.frameToShow = 1;
			end
			self.targetActor:GetController():SetState(Controller.BODY_JUMP, false);
			local facing = "A";
			if target.HFlipped then
				facing = "B";
			end
			local pos = target.Pos + Vector(0, -ToMOSprite(target):GetSpriteHeight() / 2):RadRotate(target.RotAngle);
			local wings = CreateAttachable("Wings Small ".. facing);
			for player = Activity.PLAYER_1, Activity.MAXPLAYERCOUNT - 1 do
				if not SceneMan:IsUnseen(target.Pos.X, target.Pos.Y, ActivityMan:GetActivity():GetTeamOfPlayer(player)) then
					FrameMan:DrawBitmapPrimitive(player, pos, wings, target.RotAngle, self.frameToShow);
				end
			end
		else
			if IsActor(self.targetActor) then
				self.targetActor:RemoveNumberValue("Wings");
				AudioMan:PlaySound("Mario.rte/Sounds/smb3/smb3_player_down1.wav ", SceneMan:TargetDistanceScalar(self.targetActor.Pos), false, true, -1);
			end
			self.ToDelete = true;
		end
	elseif self.FiredFrame or (self.updateTimer:IsPastSimMS(self.updateDelay) and not parent) then
		self.Frame = 0;
		self.updateDelay = 17;	-- New update delay
		self.updateTimer:Reset();
		local terrCheck = SceneMan:GetTerrMatter(self.Pos.X, self.Pos.Y + 8);
		if terrCheck ~= 0 then
			self.Vel.Y = self.Vel.Y / 2 - 1;
		end
		for actor in MovableMan.Actors do
			if actor.ClassName == "AHuman" or actor.ClassName == "ACrab" then
			--if actor.ClassName ~= "ACRocket" and actor.ClassName ~= "ACDropShip" and actor.ClassName ~= "ADoor" then
				local dist = SceneMan:ShortestDistance(actor.Pos, self.Pos, SceneMan.SceneWrapsX);
				if dist.Magnitude < (self.Radius + actor.Radius) then
					local particleCount = 3;
					for i = 1, particleCount do
						local part = CreateMOSParticle("Mario.rte/Sparkle");
						part.Pos = self.Pos + Vector(self.Radius * (i / particleCount), 0):RadRotate(6.28 * math.random());
						part.Lifetime = part.Lifetime * RangeRand(0.5, 1.0);
						MovableMan:AddParticle(part);
					end
					if actor:NumberValueExists("Wings") then
						ActivityMan:GetActivity():SetTeamFunds(ActivityMan:GetActivity():GetTeamFunds(actor.Team) + self:GetGoldValue(0, 1, 1), actor.Team);
						AudioMan:PlaySound("Base.rte/GUIs/Sounds/Poing".. math.random(6) ..".wav", SceneMan:TargetDistanceScalar(actor.Pos), false, false, -1);
						self.ToDelete = true;
					else
						AudioMan:PlaySound("Mario.rte/Sounds/smb3/smb3_power-up.wav", SceneMan:TargetDistanceScalar(actor.Pos), false, false, -1);
						actor:SetNumberValue("Wings", 1);
						actor:FlashWhite(50);
						actor.Health = actor.MaxHealth;
						local target = actor;
						if IsAHuman(actor) then
							self.targetActor = ToAHuman(actor);
							if self.targetActor.Head then
								target = self.targetActor.Head;
							end
						elseif IsACrab(actor) then
							self.targetActor = ToACrab(actor);
						else
							self.targetActor = actor;
						end
						for i = 1, particleCount do
							local part = CreateMOSParticle("Mario.rte/Sparkle");
							part.Pos = target.Pos + Vector(target.Diameter * RangeRand(0.6, 0.9), 0):RadRotate(6.28 * (i / particleCount));
							part.Lifetime = part.Lifetime * RangeRand(0.5, 1.0);
							MovableMan:AddParticle(part);
						end
						self.GetsHitByMOs = false;
						self.Scale = 0;
						self.HUDVisible = false;
						self.JointStrength = -1;
						self.Pos = Vector(0, 0);
						self.Vel = Vector(0, 0);
					end
					break;
				end
			end
		end
	elseif parent then
		self.Frame = 0;
		self.updateTimer:Reset();
		self.updateDelay = 300;
	end
	if self.sparkleTimer:IsPastSimMS(self.sparkleDelay) then
		self.sparkleTimer:Reset();
		local part = CreateMOSParticle("Mario.rte/Sparkle");
		part.Pos = target.Pos + Vector(target.Radius * RangeRand(0.8, 1.0), 0):RadRotate(6.28 * math.random());
		part.Lifetime = part.Lifetime * RangeRand(0.5, 1.0);
		MovableMan:AddParticle(part);
	end
end