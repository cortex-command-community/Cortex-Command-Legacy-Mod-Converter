function Create(self)
	self.duration = 500;	-- How many FRAMES the effect takes place for
	
	self.flashDelay = 150;
	self.flashTimer = Timer();
	
	self.updateTimer = Timer();
	self.updateDelay = 300;	-- Time window to pickup after dropped
	
	self.lastVel = Vector(self.Vel.X, self.Vel.Y);
	self.frameToShow = 0;
	
	self.heightRatio = 1;	-- Defined later to optimize sparkle effects
	self.totalRadius = self.Radius;	-- Defined later to optimize effects and hit detection
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
		if IsActor(self.targetActor) then
			if self.targetActor:GetNumberValue("Starman") > 1 then
				target = self.targetActor;
				self.targetActor:SetNumberValue("Starman", self.targetActor:GetNumberValue("Starman") - 1);
				local centerPos = self.targetActor.Pos;	-- Position detection origo halway between body and head or turret
				if self.targetActor.Head then
					centerPos = centerPos + SceneMan:ShortestDistance(self.targetActor.Pos, self.targetActor.Head.Pos, SceneMan.SceneWrapsX) / 2;
				elseif self.targetActor.Turret then
					centerPos = centerPos + SceneMan:ShortestDistance(self.targetActor.Pos, self.targetActor.Turret.Pos, SceneMan.SceneWrapsX) / 2;
				end
				if self.targetActor.Vel.Magnitude < 10 then
					self.targetActor.Status = 0;
				end
				if self.targetActor.Vel.Magnitude + math.abs(self.targetActor.AngularVel) > 500 then
					self.targetActor.Vel = self.targetActor.Vel / 2;
					self.targetActor.AngularVel = self.targetActor.AngularVel / 2;
				end
				self.targetActor.Health = self.targetActor.MaxHealth;
				self.targetActor:RemoveAnyRandomWounds(999);
				if self.targetActor.EquippedItem then
					ToMOSRotating(self.targetActor.EquippedItem):RemoveWounds(999);
				end
				-- Kill enemies
				local enemy;
				local dist = Vector(self.targetActor.Vel.X, self.targetActor.Vel.Y):SetMagnitude(self.totalRadius);
				local checkPos = centerPos + Vector(dist.X, dist.Y);
				local moCheck = SceneMan:GetMOIDPixel(checkPos.X, checkPos.Y);
				if moCheck ~= 255 then
					local mo = MovableMan:GetMOFromID(moCheck);
					local rootMO = MovableMan:GetMOFromID(mo.RootID);
					if rootMO and IsActor(rootMO) and rootMO.Team ~= self.targetActor.Team then
						enemy = ToActor(rootMO);
						dist = SceneMan:ShortestDistance(enemy.Pos, self.targetActor.Pos, SceneMan.SceneWrapsX);
					end
				else
					local actor = MovableMan:GetClosestEnemyActor(self.targetActor.Team, self.targetActor.Pos, self.targetActor.Diameter + self.targetActor.Vel.Magnitude * 0.2, dist);
					if actor and dist.Magnitude < (self.targetActor.Radius + actor.Radius + actor.Vel.Magnitude * 0.2) then
						enemy = ToActor(actor);
					end
				end
				if enemy and enemy.Status < 3 then
					enemy:FlashWhite(20);
					enemy.HitsMOs = false;
					enemy.Health = 0;
					enemy.Vel = enemy.Vel / 2 - Vector(dist.X, dist.Y / 2):SetMagnitude(self.targetActor.Vel.Magnitude + 5) - SceneMan.GlobalAcc / 2;
					AudioMan:PlaySound("Mario.rte/Sounds/smw/smw_stomp.wav", SceneMan:TargetDistanceScalar(enemy.Pos), false, true, -1);
					local particleCount = 5;	-- Star shape
					for i = 1, particleCount do
						local part = CreateMOSParticle("Mario.rte/Hit Effect Tiny Star");
						part.Lifetime = part.Lifetime * RangeRand(0.5, 1.0);
						part.Pos = enemy.Pos + dist / 2;
						part.Vel = Vector((10 + enemy.Vel.Magnitude) / 2, 0):RadRotate(1.58 + 6.28 * (i / particleCount)) + Vector(0, -5);
						MovableMan:AddParticle(part);
					end
					local glow = CreateMOPixel("Mario.rte/Hit Effect Star Glow");
					glow.Pos = enemy.Pos + dist / 2;
					MovableMan:AddParticle(glow);
				end
			else	-- Revert
				self.targetActor.MissionCritical = false;
				for i = 1 , MovableMan:GetMOIDCount() - 1 do
					local mo = MovableMan:GetMOFromID(i);
					if mo and IsMOSRotating(mo) and ToMOSRotating(mo):NumberValueExists("Starman Part") then

						mo = ToMOSRotating(mo);
						
						mo.GibWoundLimit = mo:GetNumberValue("GibWoundLimit");
						mo.GibImpulseLimit = mo:GetNumberValue("GibImpulseLimit");
						mo.DamageMultiplier = mo:GetNumberValue("DamageMultiplier");
						
						if IsAttachable(mo) then
							mo = ToAttachable(mo);
							mo.JointStrength = mo:GetNumberValue("JointStrength");
							mo.JointStiffness = mo:GetNumberValue("JointStiffness");
						end
						mo:RemoveNumberValue("Starman Part");
					end
				end
				local limbs;
				if IsAHuman(self.targetActor) then
					self.targetActor = ToAHuman(self.targetActor);
					limbs = {self.targetActor.Head, self.targetActor.FGArm, self.targetActor.BGArm, self.targetActor.FGLeg, self.targetActor.BGLeg};
				elseif IsACrab(self.targetActor) then
					self.targetActor = ToACrab(self.targetActor);
					limbs = {self.targetActor.Turret, self.targetActor.RFGLeg, self.targetActor.LFGLeg, self.targetActor.RBGLeg, self.targetActor.LBGLeg};
				end
				if limbs then
					for i = 1, #limbs do
						local limb = limbs[i];
						if limb then
							local bool = false;
							if limb:GetNumberValue("GetsHitByMOs") == 1 then
								bool = true;
							end
							limb.GetsHitByMOs = bool;
						end
					end
				end
				self.targetActor:RemoveNumberValue("Starman");
				self.targetActor:RemoveNumberValue("Starman Host");
				self.ToDelete = true;
			end
		else	-- Out of bounds
			self.targetActor = nil;
			self.ToDelete = true;
		end
	elseif self.FiredFrame or (self.updateTimer:IsPastSimMS(self.updateDelay) and not parent) then
		self.updateDelay = 17;	-- New update delay
		self.updateTimer:Reset();
		local terrCheck = SceneMan:GetTerrMatter(self.Pos.X, self.Pos.Y + 8 + self.Vel.Y * 0.2);
		if terrCheck ~= 0 then
			self.Vel = Vector(self.Vel.X * 0.9 + math.random(-2, 2) / (1 + math.abs(self.Vel.X)), -self.Vel.Y * 0.8 - 4);
		end
		for actor in MovableMan.Actors do
			if actor.ClassName == "AHuman" or actor.ClassName == "ACrab" then
			--if actor.ClassName ~= "ACRocket" and actor.ClassName ~= "ACDropShip" and actor.ClassName ~= "ADoor" then
				local dist = SceneMan:ShortestDistance(actor.Pos, self.Pos, SceneMan.SceneWrapsX);
				if dist.Magnitude < (self.Radius + actor.Radius) then
					actor:SetNumberValue("Starman", actor:GetNumberValue("Starman") / 2 + self.duration);
					AudioMan:PlaySound("Mario.rte/Sounds/smb3/smb3_power-up.wav ", SceneMan:TargetDistanceScalar(actor.Pos), false, false, -1);
					local particleCount = 3;
					for i = 1, particleCount do
						local part = CreateMOSParticle("Mario.rte/Sparkle");
						part.Pos = self.Pos + Vector(self.Radius * (i / particleCount), 0):RadRotate(6.28 * math.random());
						part.Lifetime = part.Lifetime * RangeRand(0.5, 1.0);
						MovableMan:AddParticle(part);
					end
					if actor:NumberValueExists("Starman Host") then
						self.ToDelete = true;
					else
						-- Make this object the host particle for tracking this actor
						actor:SetNumberValue("Starman Host", 1);
						self.GetsHitByMOs = false;
						self.Scale = 0;
						self.HUDVisible = false;
						self.JointStrength = -1;
						self.Pos = Vector(0, 0);
						self.Vel = Vector(0, 0);
						-- Inititate
						actor.MissionCritical = true;
						for i = 1 , MovableMan:GetMOIDCount() - 1 do
							local mo = MovableMan:GetMOFromID(i);
							if mo and IsMOSRotating(mo) and not IsHeldDevice(mo) and mo.RootID == actor.ID then

								mo = ToMOSRotating(mo);
								mo:SetNumberValue("Starman Part", 1);
								-- Save the previous values for revert
								mo:SetNumberValue("GibWoundLimit", mo.GibWoundLimit);
								mo:SetNumberValue("GibImpulseLimit", mo.GibImpulseLimit);
								mo:SetNumberValue("DamageMultiplier", mo.DamageMultiplier);
								
								mo.GibWoundLimit = 999999999;
								mo.GibImpulseLimit = 999999999;
								mo.DamageMultiplier = 0;
								
								if IsAttachable(mo) then
									mo = ToAttachable(mo);
									mo:SetNumberValue("JointStrength", mo.JointStrength);
									mo:SetNumberValue("JointStiffness", mo.JointStiffness);
									mo.JointStrength = 999999999;
									mo.JointStiffness = 0;
								end
							end
						end
						self.totalRadius = actor.Radius;
						self.heightRatio = ToMOSprite(actor):GetSpriteHeight() / ToMOSprite(actor):GetSpriteWidth();	-- To position effects etc.
						local limbs;
						if IsAHuman(actor) then
							actor = ToAHuman(actor);
							limbs = {actor.Head, actor.FGArm, actor.BGArm, actor.FGLeg, actor.BGLeg};
							if actor.Head and actor.Head.Radius > actor.Radius then
								self.totalRadius = (actor.Radius + actor.Head.Radius) / 2;
								self.heightRatio = self.heightRatio + (actor.Head.Radius / actor.Radius);
							end
						elseif IsACrab(actor) then
							actor = ToACrab(actor);
							limbs = {actor.Turret, actor.RFGLeg, actor.LFGLeg, actor.RBGLeg, actor.LBGLeg};
							if actor.Turret and actor.Turret.Radius > actor.Radius then
								self.totalRadius = (actor.Radius + actor.Turret.Radius) / 2;
								self.heightRatio = self.heightRatio + (actor.Turret.Radius / actor.Radius);
							end
						end
						if limbs then
							for i = 1, #limbs do
								local limb = limbs[i];
								if limb then
									if limb.GetsHitByMOs then
										limb:SetNumberValue("GetsHitByMOs", 1);
									end
									limb.GetsHitByMOs = false;	-- This is the only way to prevent limbs from breaking
								end
							end
						end
						self.targetActor = actor;
						target = self.targetActor;
					end
					break;
				end
			end
		end
	elseif parent then
		self.updateTimer:Reset();
		self.updateDelay = 300;
	end
	if self.flashTimer:IsPastSimMS(self.flashDelay) then
		self.flashTimer:Reset();
		if self.targetActor then
			self.targetActor:FlashWhite(self.flashDelay / 2);
		end
		self.frameToShow = self.frameToShow + 1;
		if self.frameToShow == self.FrameCount then
			self.frameToShow = 0;
		end
		local particleCount = 1 + target.Radius / 5;
		local rand = 6.28 * math.random();
		for i = 1, particleCount do
			local part = CreateMOSParticle("Mario.rte/Sparkle");
			local vector = Vector(self.totalRadius * RangeRand(0.8, 1.0), 0):RadRotate(rand + 6.28 * (i/particleCount))
			if self.heightRatio ~= 1 then
				vector = Vector(vector.X, vector.Y * self.heightRatio):RadRotate(target.RotAngle);
			end
			part.Pos = target.Pos + vector;
			part.Lifetime = part.Lifetime * RangeRand(0.5, 1.0);
			MovableMan:AddParticle(part);
		end
	end
	self.Frame = self.frameToShow;
end