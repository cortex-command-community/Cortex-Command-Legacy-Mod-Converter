-- It's a-me!
function Create(self)
	self.stompPower = 1.5;	-- How many times bigger object Mario can stomp
	self.stompBoost = 5;	-- How much aerial boost Mario gains from a stomp

	self.dead = false;

	self.startSound = {"mario-haha", "mario-hello", "mario-herewego", "mario-itsme", "mario-letsgo", "mario-okiedokie"};
	self.hurtSound = {"mario-hello", "mario-herewego", "mario-imtired", "mario-letsgo", "mario-lowonhealth", "mario-mamamia"};
	self.painSound = {"mario-oof", "mario-pain"};
	self.dyingSound = {"mario-cough", "mario-die"};
	self.jumpSound = {"mario-wa", "mario-ya"};
	self.killSound = {"mario-buhbye", "mario-gameover", "mario-haha", "mario-solongbowser", "mario-woohoo"};
	
	self.flySound = {"mario-waha", "mario-yahoo", "mario-yippee"};

	self.soundTimer = Timer();
	self.soundDelay = 1100;
	
	self.killTimer = Timer();
	self.airTimer = Timer();

	self.lastHealth = 100;
	local actor = MovableMan:GetMOFromID(self.RootID);
	if actor and IsAHuman(actor) then
		self.parent = ToAHuman(actor);
		self.lastHealth = self.parent.Health;	
	end
	local sound;
	if self.Vel.Magnitude > 25 then
		sound = self.flySound;
	elseif MarioEntered ~= true then
		MarioEntered = true;
		sound = self.startSound;
	end
	self.playerControlled = false;
	if sound then
		AudioMan:PlaySound("Mario.rte/Sounds/sm64/".. sound[math.random(#sound)] ..".wav ", SceneMan:TargetDistanceScalar(self.Pos), false, false, -1);
	end
end

function Update(self)
	self.negNum = 1;
	if self.HFlipped then
		self.negNum = -1;
	end
	self.Frame = 1;
	local sound;
	if self.parent then
		if not IsActor(self.parent) or self.parent.Status > 2 then
			if self.dead == false then
				sound = self.deathSound;
				self.soundDelay = 3000;
			end
			self.dead = true;
		else
			if self.parent.Status == 1 then
				self.Frame = 1;
			else
				self.Frame = 0;
				local item = self.parent.EquippedItem;
				local length = 0;
				if item then
					if IsHDFirearm(item) then
						length = ToHDFirearm(item).SharpLength;
					end
					if self.parent:GetController():IsState(Controller.WEAPON_FIRE) then
						self.killTimer:Reset();
					end
				end
				if self.parent:IsPlayerControlled() and not self.killTimer:IsPastSimMS(5000) then
					local dist = Vector(0, 0);
					length = length + (FrameMan.ResY + FrameMan.ResX) / 2;
					local actor = MovableMan:GetClosestEnemyActor(self.parent.Team, self.Pos, length, dist);
					if actor and actor.Status > 2 then
						local terrRay = SceneMan:CastStrengthRay(actor.Pos, dist, 20, Vector(), math.sqrt(dist.Magnitude), 0, SceneMan.SceneWrapsX);
						if not(terrRay) then
							sound = self.killSound;
							self.soundDelay = 1200;
						end
					end
				end
				if (self.parent.FGLeg or self.parent.BGLeg) then
					local dir = 0;
					if self.parent:GetController():IsState(Controller.MOVE_LEFT) then
						dir = dir - 1;
					end
					if self.parent:GetController():IsState(Controller.MOVE_RIGHT) then
						dir = dir + 1;
					end
					if dir ~= 0 then
						self.parent.Vel.X = self.parent.Vel.X + dir / (3 + math.abs(self.parent.Vel.X) * 3);
					end
					if self.parent:GetController():IsState(Controller.BODY_JUMPSTART) then
						local checkPos = self.parent.Pos - Vector(self.parent.Vel.X, self.parent.Vel.Y - 25):SetMagnitude(self.parent.Radius + 2);
						local terrCheck = SceneMan:GetTerrMatter(checkPos.X, checkPos.Y);
						if terrCheck ~= 0 then
							local mat = SceneMan:GetMaterialFromID(terrCheck);
							local sfx = "step-floor";
							if mat.StructuralIntegrity < 60 then
								sfx = "step-grass";
							end
							AudioMan:PlaySound("Mario.rte/Sounds/sm64/".. sfx ..".wav ", SceneMan:TargetDistanceScalar(checkPos), false, true, -1);
						end
					elseif self.parent.Vel.Magnitude > 5 and self.parent.Vel.Y > 0 then
						local checkPos = self.parent.Pos + Vector(self.parent.Vel.X, self.parent.Vel.Y + 10):SetMagnitude(self.parent.Radius + self.parent.Vel.Magnitude * 0.2);
						local moCheck = SceneMan:GetMOIDPixel(checkPos.X, checkPos.Y);
						if moCheck ~= 255 then
							local mo = MovableMan:GetMOFromID(moCheck);
							if mo and IsMOSRotating(mo) and mo.Team ~= self.parent.Team then
								local sfx = "smw/smw_stomp_no_damage";
								if (mo.Mass + mo.Radius + mo.Vel.Y) / self.stompPower < (self.parent.Mass + self.parent.Radius + self.parent.Vel.Y) then
									mo.Vel.Y = mo.Vel.Y / 2 + self.parent.Vel.Y + self.stompBoost / 2;
									ToMOSRotating(mo):GibThis();
									self.parent.Vel.Y = -self.parent.Vel.Y / 2 - self.stompBoost;
									if self.parent.Vel.Magnitude > 20 then
										sound = self.flySound;
										self.soundDelay = 1100;
									end
									sfx = "smw/smw_stomp";
									--sfx = "smb3/smb3_stomp_+8db";
									local particleCount = 4;
									for i = 1, particleCount do
										local part = CreateMOSParticle("Mario.rte/Hit Effect Tiny Star");
										part.Lifetime = part.Lifetime * RangeRand(0.5, 1.0);
										part.Pos = checkPos;
										part.Vel = Vector((self.stompBoost + self.parent.Vel.Magnitude) / 2, 0):RadRotate(0.79 + 6.28 * (i / particleCount)) + Vector(0, -self.stompBoost / 2);
										MovableMan:AddParticle(part);
									end
								else
									mo.Vel.Y = mo.Vel.Y + self.parent.Vel.Y / math.sqrt(math.abs(mo.Mass) + 1);
									self.parent.Vel.Y = -self.parent.Vel.Y / 2 - 5;
								end
								if math.random() < 0.01 then
									sfx = "sm64/mario-boing";
								end
								local glow = CreateMOPixel("Mario.rte/Hit Effect Star Glow");
								glow.Pos = checkPos;
								MovableMan:AddParticle(glow);
								AudioMan:PlaySound("Mario.rte/Sounds/".. sfx ..".wav ", SceneMan:TargetDistanceScalar(checkPos), false, true, -1);
							end
						end
					end
				else
					self.parent:GetController():SetState(Controller.BODY_JUMPSTART, false);
					self.parent:GetController():SetState(Controller.BODY_JUMP, false);
					if self.parent.Jetpack then
						self.parent.Jetpack.ToDelete = true;
					end
				end
			end
			if self.parent:IsPlayerControlled() then
				if self.playerControlled == false then
					sound = self.startSound;
					self.soundDelay = 1300;
					if self.parent.Health < self.parent.MaxHealth / 2 then
						sound = self.hurtSound;
						self.soundDelay = 1100;
					end
				end
				self.playerControlled = true;
			else
				self.playerControlled = false;
			end
			if self.parent.Health < self.lastHealth - 1 then
				if self.fallSFX and MovableMan:IsParticle(self.fallSFX) then
					self.fallSFX.ToDelete = true;
					self.fallSFX = nil;
				end
				sound = self.painSound;
				self.soundDelay = 700;
				self.Frame = 1;
			end
		end
		self.lastHealth = self.parent.Health;
		if sound and self.soundTimer:IsPastSimMS(self.soundDelay) then
			self.soundTimer:Reset();
			AudioMan:PlaySound("Mario.rte/Sounds/sm64/".. sound[math.random(#sound)] ..".wav ", SceneMan:TargetDistanceScalar(self.Pos), false, false, -1);
		elseif self.dead == false then
			local totalAir = self.parent.Vel.Magnitude + math.abs(self.parent.AngularVel);
			if self.fallSFX and MovableMan:IsParticle(self.fallSFX) then
				self.fallSFX.Pos = self.Pos;
				if totalAir < 10 then
					self.fallSFX.ToDelete = true;
					self.fallSFX = nil;
				end
			elseif totalAir > 25 then
				if self.airTimer:IsPastSimMS(20000 / totalAir) then
					self.fallSFX = CreateAEmitter("Mario.rte/Mario Scream");
					--[[
					if (math.abs(self.parent.Vel.X) - self.parent.Vel.Y) < 0 then
						self.fallSFX = CreateAEmitter("Mario Fall Sound");
					end
					]]--
					self.fallSFX.Pos = self.Pos;
					self.fallSFX.Team = self.Team;
					MovableMan:AddParticle(self.fallSFX);
				end
			else
				self.fallSFX = nil;
				self.airTimer:Reset();
			end
		end
	else
		local parent = self:GetParent();
		if parent and IsAHuman(parent) then
			self.parent = ToAHuman(parent);
		end
	end
end

function Destroy(self)
	MarioEntered = false;
	if self.fallSFX and MovableMan:IsParticle(self.fallSFX) then
		self.fallSFX.ToDelete = true;
	end
end