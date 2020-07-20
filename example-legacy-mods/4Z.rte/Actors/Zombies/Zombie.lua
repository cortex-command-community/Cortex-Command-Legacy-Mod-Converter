
--	dofile("Base.rte/Constants.lua")	--
--	require("Actors/AI/NativeHumanAI") 	-- not required, actually functions better without these

--------------------------------------
--------------------------------------
--	zombie actor by 4zK				--
--	features:						--
--		static melee attack			--
--		flaily arms	and head		--
--		rip your limbs out?!		--
--		"fake death" surprise		--
--		blood spray decapitation	--
--		climbing terrain and MOs	--
--		other small things! enjoy!	--
--------------------------------------
--------------------------------------

function Create(self)

	self.Frame = math.random(0, 1);

	self.num = 1;
	self.rotNum = 1;

	self.hurtTimer = Timer();
	self.enemyClose = 0;

	self.lastHealth = self.Health;
	self.lastWoundCount = self.TotalWoundCount;
	self.deathSound = false;

	self.idleOffset = {0, 0, 0, 0};	-- 1 = FGLength, 2 = FGAngle, 3 = BGLength, 4 = BGAngle
	self.lastBGArmAngle = 0;
	self.updTimerSlow = Timer();	-- updates move paths and legless damage
	self.updTimerFast = Timer();	-- updates arm flail and walk stutter

	self.KOlimit = 0.4;		-- percent of drop in HP to knock out
	self.KOchance = 0.2;	-- percent of additional chance for KO
	self.KOtime = 30;		-- maximum KO time in seconds, minimum is 10% of maximum

	self.fakeDeath = false;
	self.fakeTimer = Timer();
	
	self.climbTimer = Timer();
	
	self.width = ToMOSprite(self):GetSpriteWidth();
	self.height = ToMOSprite(self):GetSpriteHeight();
	
	self.walkSpeed = self:GetLimbPathSpeed(1)
	self:SetLimbPathSpeed(1, self.walkSpeed * RangeRand(0.9, 1.1));
	
	self.GibWoundLimit = self.GibWoundLimit * 1.25;
	
	if string.find(self.PresetName, "Bloater") then
		self.Frame = 0;	-- full
		self.explosion = CreateAEmitter("Bloater Goo Explosion");
	end
end

function Update(self)

	self.negNum = self.HFlipped and -1 or 1;
	self.ctrl = self:GetController();

	if self.Status < 3 then
		if self.fakeDeath then
			-- they can lay emotionless but still remain alive (gotta have head tho)
			-- to revive, either: 1) press jump 2) get healed 3) wait until timer runs out
			if (self.ctrl:IsState(Controller.BODY_JUMPSTART) and self:IsPlayerControlled()) or self.Health > self.lastHealth or self.fakeTimer:IsPastSimMS(math.abs(self.KOtime * 1000 - (self.KOtime * self.Health))) then
				self.Status = 1;	-- revive
				self.fakeDeath = false;
			else
				self.Status = 2;						-- stay emotionless
				if self.BGArm then
					self.BGArm.RotAngle = self.lastBGArmAngle;	-- it spins for some reason (pls stay still boi)
				end
				self.ctrl:SetState(Controller.BODY_JUMP, false);
				self.ctrl:SetState(Controller.BODY_JUMPSTART, false);
				self.ctrl:SetState(Controller.MOVE_LEFT, false);
				self.ctrl:SetState(Controller.MOVE_RIGHT, false);
				self.HUDVisible = false;
			end
		else
			local flail = 0.2;
			if self.Head then
				if math.random() < self.KOchance and self.Health < self.lastHealth * (1 - self.KOlimit) then	-- chances of KO
					self.Health = math.min(self.Health + (self.KOlimit) * 50, self.MaxHealth - 1);	-- heal slightly

					self.fakeDeath = true;
					self.fakeTimer:Reset();

					if self.BGArm then
						self.lastBGArmAngle = self.BGArm.RotAngle;
					end
					self:DropAllInventory();
					self.Status = 1;	-- dislodge
					self.AngularVel = self.AngularVel - 5 * self.negNum;	-- fall
				end
				if self.ctrl:IsState(Controller.WEAPON_FIRE) or self.enemyClose > 0 then
					flail = flail + self.Health / (200 + 10 * math.sqrt(self.enemyClose));
					if self.stolenLimb == nil then

						if self.Status < 3 and self.hurtTimer:IsPastSimMS(math.abs(800 - self.Health * 4)) then
							-- pick the MO that spews damage
							local attackMO = self.Head;
							-- use arm if available
							if self.FGArm and math.random() < 0.5 then
								attackMO = self.FGArm;
							elseif self.BGArm then
								attackMO = self.BGArm;
							end
						
							local dmg = CreateMOPixel("Particle Claw ".. math.random(2), "4Z.rte");			-- bite
							dmg.Pos = attackMO.Pos;
							dmg.Vel = self.Vel + Vector(50 * self.negNum, 0):RadRotate(attackMO.RotAngle);
							dmg.Team = self.Team;
							dmg.IgnoresTeamHits = true;
							MovableMan:AddParticle(dmg);
						
							if self.ctrl:IsState(Controller.WEAPON_FIRE) and self.FGArm then

								local mocheck = SceneMan:GetMOIDPixel(ToArm(self.FGArm).HandPos.X, ToArm(self.FGArm).HandPos.Y);
													--SceneMan:CastMORay(ToArm(self.FGArm).HandPos,
													--Vector(3 * self.negNum, 0):RadRotate(self:GetAimAngle(false)),
													--self.ID, self.Team, 0, true, 0);
								if mocheck ~= 255 then
									local mo = MovableMan:GetMOFromID(mocheck);
									if mo and mo.Team ~= self.Team and IsAttachable(mo) and ToAttachable(mo):IsAttached() then

										mo = ToAttachable(mo);
										local a = mo.Mass + mo.JointStrength;	-- 
										local b = (self.Mass + self.Health) + 1;	--
										if math.random() > a / b then	-- chances
										--if a < b then			-- conditions

											self.origLimbJstr = mo.JointStrength;
											mo.JointStrength = -1;		-- detach
											mo.Team = self.Team;	-- doesn't work?
											self.origLimbHUD = mo.HUDVisible;	--
											mo.HUDVisible = false;			-- for items

											self.tsAngle = self.FGArm.RotAngle;	-- arm angle when sticking	
											self.sAngle = mo.RotAngle;		-- mo angle when sticking	

											self.sPosX = (self.FGArm.Pos.X-mo.Pos.X) * 0.7;	-- for closing the distance a bit
											self.sPosY = (self.FGArm.Pos.Y-mo.Pos.Y) * 0.7;

											mo.Pos = self.FGArm.Pos - Vector(self.sPosX,self.sPosY);

											self.stolenLimb = mo;
											self:SetWhichMOToNotHit(self.stolenLimb, -1);	--
										end
									end
								end
							end
							self.hurtTimer:Reset();
						end
					else
						if self.stolenLimb.ID ~= 255
						and self.stolenLimb.RootID == self.stolenLimb.ID
						and self.FGArm then

							self.FGArm.Mass = 20 + self.stolenLimb.Mass;	-- some weight to carry around

							self.stolenLimb.ToSettle = false;
							self.stolenLimb.JointStrength = self.origLimbJstr;	--
							self.stolenLimb.HUDVisible = false;			-- for items

							self.stolenLimb.PinStrength = 1000;
							self.stolenLimb.AngularVel = self.AngularVel;	--
							self.stolenLimb.Vel = self.Vel;			--

							self.stolenLimb.Pos = ToArm(self.FGArm).HandPos + Vector(self.stolenLimb.Radius*0.0*self.negNum,self.sPosY):RadRotate(self.FGArm.RotAngle);
							self.stolenLimb.RotAngle = self.tsAngle + (self.FGArm.RotAngle - self.sAngle);

							--[[if self.ctrl:IsState(Controller.WEAPON_FIRE) and self:IsPlayerControlled() then
								self.stolenLimb.PinStrength = 0;
								local velNum = math.sqrt(math.abs(self.stolenLimb.Mass/3)+1);
								self.stolenLimb.Vel = Vector(self.Health*0.2/velNum*self.negNum,-self.Health*0.1/velNum):RadRotate(self:GetAimAngle(false));
								self.stolenLimb.IgnoresTeamHits = false;	-- hit friend (enemy)
								self.stolenLimb.HUDVisible = self.origLimbHUD;
								self.stolenLimb = nil;
								self.FGArm.Mass = 20;
							end]]--
						else
							self.stolenLimb.PinStrength = 0;
							self.stolenLimb.HUDVisible = self.origLimbHUD;
							self.stolenLimb.JointStrength = self.origLimbJstr;	--
							self.stolenLimb = nil;
							self.FGArm.Mass = 20;
						end
					end
				end
				self.rotNum = self.rotNum + math.random() * math.random();
				if not self.ctrl:IsState(Controller.AIM_SHARP) then
					self.Head.RotAngle = -(math.sin(self.rotNum) * 0.2 - self:GetAimAngle(false)) * self.negNum;
				end
			else	-- if not self.Head then
				if self.deathSound == false then

					self.Health = self.lastHealth - math.random(5, 40);	-- instant 5-40 damage from head loss
					self.lastHealth = self.Health;

					local sfx = CreateAEmitter("4Zombie Death Sound", "4Z.rte");
					sfx.Pos = self.Pos;
					sfx.Team = self.Team;
					sfx.IgnoresTeamHits = true;
					MovableMan:AddParticle(sfx);

					self.deathSound = true;
				end
				-- add 3 points of damage for every new wound and half mass equivalent for lost limbs
				local damage = -math.abs((self.TotalWoundCount - self.lastWoundCount) * 3 + math.floor(self.lastMass - self.Mass) / 2);
				self.Health = self.lastHealth - 1 + damage;	-- delayed decap death..... spoopy
				
				flail = flail * 2 + self.Health / 100;
			end
			-- flail arms
			for i = 1, #self.idleOffset do
				self.idleOffset[i] = self.idleOffset[i] + math.random() * flail;
			end
			if self.FGArm then
				ToArm(self.FGArm).IdleOffset = Vector(11 + math.sin(self.idleOffset[1]) + flail, 3):RadRotate(self:GetAimAngle(false) + math.sin(self.idleOffset[2]) * flail);
			end
			if self.BGArm then
				if not self.FGArm and self.BGArm.GetsHitByMOs == false then
					self.BGArm.GetsHitByMOs = true;
				else
					self.BGArm.GetsHitByMOs = false;
				end
				ToArm(self.BGArm).IdleOffset = Vector(11 + math.sin(self.idleOffset[3]) + flail, -1):RadRotate(self:GetAimAngle(false) + math.sin(self.idleOffset[4]) * flail);
			end
		end
		if self.FGLeg and self.BGLeg then
			if self.ctrl:IsState(Controller.BODY_JUMPSTART) then
				self.ctrl:SetState(Controller.BODY_CROUCH, true);	-- lunge jump
			elseif self.Health < self.MaxHealth then
				self.ctrl:SetState(Controller.BODY_CROUCH, false);	-- otherwise stand up
			end
		else	-- can only jump with both legs
			if self.Jetpack then
				self.Jetpack.ToDelete = true;
				self:SetLimbPathSpeed(1, self.walkSpeed / 2);
			end
			self.ctrl:SetState(Controller.BODY_JUMP, false);
			self.ctrl:SetState(Controller.BODY_JUMPSTART, false);
			if math.random() < 0.9 then
				self.ctrl:SetState(Controller.BODY_CROUCH, true);
			end
		end
		if self.EquippedItem and self.ctrl:IsState(Controller.WEAPON_FIRE) then
			local rand = math.random();
			if rand < 0.1 then
				self.ctrl:SetState(Controller.WEAPON_DROP, true);
			elseif rand < 0.2 then
				ToMOSRotating(self.EquippedItem):GibThis();
			end
		end
			
		---- thanks CC48 for original climb script!
		local wallCheck;
		
		if self.climbTimer:IsPastSimMS(40) then	-- reduce performance loss
			self.climbTimer:Reset();
			
			local moved, climbMO = false, false;
			local trace = Vector(0, self.height * 0.8):RadRotate(RangeRand(-0.1, 0.1));
			local moRay = SceneMan:CastMORay(self.Pos, trace, self.ID, -2, 0, false, math.random(self.height * 0.4));
	
			if moRay ~= 255 then
				local mo = MovableMan:GetMOFromID(moRay);
				if mo.Team == self.Team then
					climbMO = true;
				end
			end
			
			local frontCheckPos = self.Pos + Vector(self.width * self.negNum, 0);
			wallCheck = SceneMan:GetTerrMatter(frontCheckPos.X, frontCheckPos.Y) ~= 0;

			if (self.ctrl:IsState(Controller.MOVE_LEFT) or self.ctrl:IsState(Controller.MOVE_RIGHT)) or self.ctrl:IsState(Controller.BODY_JUMP) then
				moved = true;
			else
				moved = false;
			end
			if not self.ctrl:IsState(Controller.BODY_CROUCH) and moved then
				if climbMO or wallCheck then
					self.Vel = self.Vel * 0.9 + (Vector(1, 0):RadRotate(self:GetAimAngle(true)) - Vector(0, 1)) / (1 + self.Vel.Magnitude * 0.1);
				end
			end
		end
		if not(wallCheck) and not self.ctrl:IsState(Controller.BODY_CROUCH) then
			if math.abs(self.AngularVel) < 20 and self.Status < 1 then	-- don't spin to death okay
				-- "hunch" n stagger a bit
				self.AngularVel = self.AngularVel - (0.3 * math.random() - (self:GetAimAngle(false)) * 0.1) * self.negNum;
			end
		end
		----
		if self.updTimerSlow:IsPastSimMS(1000) then
			self.updTimerSlow:Reset();
			self:UpdateMovePath();
			if self.AIMode ~= Actor.AIMODE_BRAINHUNT then
				self.AIMode = Actor.AIMODE_BRAINHUNT;
			end
			if not (self.FGLeg and self.BGLeg) then
				self.Health = self.Health - 1;
			end
		end
		if self.updTimerFast:IsPastSimMS(300) then
			self.updTimerFast:Reset();
			self.enemyClose = 0;
			local dist = Vector(0, 0);
			if MovableMan:GetClosestEnemyActor(self.Team, self.Pos, self.Health, dist) then
				self.enemyClose = dist.Magnitude;
			end
			self:SetLimbPathSpeed(1, self.walkSpeed * RangeRand(0.75, 1.25));
		end
	else
		if self.deathSound == false then
			local sfx = CreateAEmitter("4Zombie Death Sound", "4Z.rte");
			sfx.Pos = self.Pos;
			sfx.Team = self.Team;
			sfx.IgnoresTeamHits = true;
			MovableMan:AddParticle(sfx);

			self.deathSound = true;

			self.Status = 3;	-- body die
			self.HUDVisible = false;
		end
		self.HitsMOs = false;	-- so that body won't fuckin bury you
	end
	self.ctrl:SetState(Controller.AIM_SHARP, false);
	self.ctrl:SetState(Controller.WEAPON_PICKUP, false);
	
	self.lastHealth = self.Health;
	self.lastWoundCount = self.TotalWoundCount;
	self.lastMass = self.Mass;		-- lost limbs?
	-- boomer drain code
	if self.WoundCount ~= 0 then
		if self.explosion then
			if not self.drainTimer then
				self.drainTimer = Timer();
				self.drainTime = 3000;
			elseif self.drainTimer:IsPastSimMS(self.drainTime / math.sqrt(self.WoundCount)) then
				-- boomer is drained
				self.explosion = nil;
				self.drainTimer = nil;
				self.Frame = 1;	-- empty
				self:SetEntryWound("Wound 4Zombie Entry", "4Z.rte");
				self:SetExitWound("Wound 4Zombie Exit", "4Z.rte");
				
				self.GibWoundLimit = self.GibWoundLimit + 10;
				self.GibImpulseLimit = self.GibImpulseLimit + 1000;
				self.Mass = self.Mass - 10;
			end
		-- better gib action for those not about to explode
		elseif self.WoundCount > (self.GibWoundLimit * 0.8) then
			self.GibWoundLimit = self.GibWoundLimit + 1;
			local parts = {self.FGArm, self.FGLeg, self.BGArm, self.BGLeg, self.Head};	-- priority order
			for i = 1, #parts do
				local part = parts[i];
				if part and part.WoundCount > 0 then
					part.JointStrength = -1;
					break;
				end
			end
		end
	end
end
function Destroy(self)
	if self.explosion and not self.ToSettle then
		self.explosion.Pos = Vector(self.Pos.X, self.Pos.Y);
		self.explosion.Vel = Vector(self.Vel.X, self.Vel.Y);
		self.explosion.Team = self.Team;
		MovableMan:AddParticle(self.explosion);
	end
end