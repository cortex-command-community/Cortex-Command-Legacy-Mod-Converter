function Create(self)
	self.moveSpeed = 5;
	self.updateTimer = Timer();
	self.updateDelay = 300;	-- Time window to pickup after dropped
	
	self.sparkleTimer = Timer();
	self.sparkleDelay = 500;
end
function Update(self)
	self.Vel.X = self.moveSpeed * (self.Vel.X / math.abs(self.Vel.X));
	self.AngularVel = self.AngularVel / 2;---(self.Vel.X / math.abs(self.Vel.X));
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
		local respawn;
		if IsActor(self.targetActor) then
			if self.targetActor.Status > 2 then
				self.targetActor.ToDelete = true;
				respawn = true;
			else
				target = self.targetActor;
				local icon = CreateHDFirearm(self.PresetName);
				if IsAHuman(self.targetActor) then
					self.newActor = CreateAHuman(self.targetActor:GetModuleAndPresetName());
					if self.newActor.Head then
						icon = CreateAttachable(self.newActor.Head:GetModuleAndPresetName());
					else
						icon = self.newActor;
					end
				elseif IsACrab(self.targetActor) then
					self.newActor = CreateACrab(self.targetActor:GetModuleAndPresetName());
					icon = self.newActor;
				else
					self.newActor = CreateActor(self.targetActor:GetModuleAndPresetName());
					icon = self.newActor;
				end
				self.newActor.Pos = self.targetActor.Pos;
				self.newActor.Vel = self.targetActor.Vel;
				self.newActor.AngularVel = self.targetActor.AngularVel;
				self.newActor.RotAngle = self.targetActor.RotAngle;
				self.newActor.Team = self.targetActor.Team;
				self.newActor.HFlipped = self.targetActor.HFlipped
				self.newActor.AIMode = self.targetActor.AIMode;
				self.newActor.Status = 1;
				self.newActorLives = self.targetActor:GetNumberValue("1UPs");
				self.player = self.targetActor:GetController().Player;
				--[[
				if self.targetActor:IsPlayerControlled() then	-- Display lives on top of the screen
					local scrollTarget = SceneMan:GetScrollTarget(ActivityMan:GetActivity():ScreenOfPlayer(self.player));
					local cornerPos = scrollTarget - Vector(FrameMan.PlayerScreenWidth, FrameMan.PlayerScreenHeight) / 2;
					FrameMan:DrawBitmapPrimitive(self.player, cornerPos + Vector(10, 10), icon, 0, 0);
					FrameMan:DrawTextPrimitive(self.player, cornerPos + Vector(20, 10), "".. self.newActorLives, false, 0);
				end]]--
			end
		else
			respawn = true;
		end
		if respawn then
			if self.newActor then
				-- Account for out-of-bounds deaths
				if self.newActor.Pos.Y > SceneMan.SceneHeight + 50 then
					self.newActor.Pos.Y = SceneMan.SceneHeight + 50;	self.newActor.AngularVel = -self.newActor.AngularVel;
					self.newActor.Vel = Vector(-self.newActor.Vel.X, -self.newActor.Vel.Y / math.sqrt(math.abs(self.newActor.Vel.Y)) - 10);
				elseif self.newActor.Pos.Y < -500 then
					self.newActor.Pos.Y = -500;	self.newActor.AngularVel = -self.newActor.AngularVel;
					self.newActor.Vel = Vector(-self.newActor.Vel.X, -self.newActor.Vel.Y / math.sqrt(math.abs(self.newActor.Vel.Y)) + 10);
				elseif SceneMan.SceneWrapsX == false then
					if self.newActor.Pos.X > SceneMan.SceneWidth + 50 then
						self.newActor.Pos.X = SceneMan.SceneWidth + 50;	self.newActor.AngularVel = -self.newActor.AngularVel;
						self.newActor.Vel = Vector(-self.newActor.Vel.X + 10 / math.sqrt(math.abs(self.newActor.Vel.X)), -self.newActor.Vel.Y);
					elseif self.newActor.Pos.X < -50 then
						self.newActor.Pos.X = -50;	self.newActor.AngularVel = -self.newActor.AngularVel;
						self.newActor.Vel = Vector(-self.newActor.Vel.X - 10 / math.sqrt(math.abs(self.newActor.Vel.X)), -self.newActor.Vel.Y);
					end
				else
					self.newActor.Vel = self.newActor.Vel / 2 + Vector(0, -5);
				end
				MovableMan:AddActor(self.newActor);
				self.newActor:FlashWhite(75);
				local particleCount = 3 + self.newActor.Radius / 3;
				for i = 1, particleCount do
					local part = CreateMOSParticle("Mario.rte/Sparkle");
					part.Pos = self.newActor.Pos + Vector(self.newActor.Diameter * (i / particleCount), 0):RadRotate(6.28 * math.random());
					part.Lifetime = part.Lifetime * RangeRand(0.5, 1.0);
					MovableMan:AddParticle(part);
				end
				ToGameActivity(ActivityMan:GetActivity()):SwitchToActor(self.newActor, self.player, self.newActor.Team);
				AudioMan:PlaySound("Mario.rte/Sounds/smb3/smb3_player_down1.wav ", SceneMan:TargetDistanceScalar(self.newActor.Pos), false, false, -1);
				if self.newActorLives > 1 then
					self.newActor:SetNumberValue("1UPs", self.newActorLives - 1);
					self.newActor:SetNumberValue("1UPs Host", 1);
				else
					self.newActor:RemoveNumberValue("1UPs");
					self.newActor:RemoveNumberValue("1UPs Host");
					self.ToDelete = true;
				end
				self.targetActor = ToActor(self.newActor);
			else
				print("ERROR! CANNOT SPAWN");
				self.ToDelete = true;
			end
		end
	elseif self.FiredFrame or (self.updateTimer:IsPastSimMS(self.updateDelay) and not parent) then
		self.updateDelay = 17;	-- New update delay
		self.updateTimer:Reset();
		local terrCheck = SceneMan:GetTerrMatter(self.Pos.X, self.Pos.Y + 8);
		if terrCheck ~= 0 then
			self.Vel.Y = self.Vel.Y / 2 - 1;	-- Lift from ground
		end
		for actor in MovableMan.Actors do
			if actor.ClassName == "AHuman" or actor.ClassName == "ACrab" then
			--if actor.ClassName ~= "ACRocket" and actor.ClassName ~= "ACDropShip" and actor.ClassName ~= "ADoor" then
				local dist = SceneMan:ShortestDistance(actor.Pos, self.Pos, SceneMan.SceneWrapsX);
				if dist.Magnitude < (self.Radius + actor.Radius) then
					actor:SetNumberValue("1UPs", actor:GetNumberValue("1UPs") + 1);
					AudioMan:PlaySound("Mario.rte/Sounds/smb3/smb3_1-up.wav ", SceneMan:TargetDistanceScalar(actor.Pos), false, false, -1);
					local particleCount = 3;
					for i = 1, particleCount do
						local part = CreateMOSParticle("Mario.rte/Sparkle");
						part.Pos = self.Pos + Vector(self.Radius * (i / particleCount), 0):RadRotate(6.28 * math.random());
						part.Lifetime = part.Lifetime * RangeRand(0.5, 1.0);
						MovableMan:AddParticle(part);
					end
					local part = CreateMOSParticle("Mario.rte/1UP Effect");
					part.Pos = self.AboveHUDPos + Vector(0, 5);
					MovableMan:AddParticle(part);
					actor:FlashWhite(50);
					if actor:NumberValueExists("1UPs Host") then
						self.ToDelete = true;
					else
						-- Make this object the host particle for tracking this actor
						actor:SetNumberValue("1UPs Host", 1);
						self.targetActor = actor;
						target = self.targetActor;
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