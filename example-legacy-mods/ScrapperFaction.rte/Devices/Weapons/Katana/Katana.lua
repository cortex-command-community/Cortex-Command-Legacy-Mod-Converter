
function Create(self)

	self.negNum = 1;
	self:SetNumberValue("Fire Upgrade", 1);
	self:SetNumberValue("Striking", 0);
	self:SetNumberValue("Recovery", 0);
	self:SetNumberValue("Block Mode", 0);
	self:SetNumberValue("Down Twirl", 1)
	self:SetNumberValue("Up Twirl", 0)
	self:SetNumberValue("Actively Blocking", 0)
	
	self.num = 0;
	self.num2 = 0;
	self.rotNum = 0;
	self.lastAngle = 0;
	self.rof = self.RateOfFire;
	self.psr = self.ParticleSpreadRange;
	self.lastWounds = 0;
	self.blockedWounds = 0;
	self.regenTimer = Timer();

	self.fired = false;

	self.strikeTimer = Timer();
	self.strikeTimerReset = false;
	self.recoveryTimer = Timer();
	self.blockTimer = Timer();
	self.blockingTimer = Timer();
	self.twirlTimer = Timer();
	self.parryTimer = Timer();
end

function Update(self)

	local actor
	local rotang
	local parent
	actor = MovableMan:GetMOFromID(self.RootID);
	if actor and IsAHuman(actor) then
		
		parent = ToAHuman(actor);
		
	end
	
	self.RateOfFire = 60;
	
	if self:GetNumberValue("HaveToResetNum") == 1 then
		self.num = 0;
		self.num2 = 0;
		self:SetNumberValue("HaveToResetNum", 0)
	end

	if math.random(100) < 5 and self:GetNumberValue("Fire Upgrade") == 2 then
	
		for i = 1, 1 do
			Effect = CreateMOSParticle("Tiny Smoke Ball 1", "Base.rte")
			if Effect then
				Effect.Pos = self.Pos + Vector(0,2):RadRotate(self.RotAngle)
				Effect.Vel = (self.Vel / 5) - Vector(2*self.negNum,0):RadRotate(self.RotAngle)
				MovableMan:AddParticle(Effect)
			end
		end

		for i = 1, 1 do
			Effect = CreateMOSParticle("Tiny Smoke Ball 1", "Base.rte")
			if Effect then
				Effect.Pos = self.Pos + Vector(0,0):RadRotate(self.RotAngle)
				Effect.Vel = (self.Vel / 5) - Vector(7*self.negNum,0):RadRotate(self.RotAngle)
				MovableMan:AddParticle(Effect)
			end
		end
		
		for i = 1, 1 do
			Effect = CreateMOSParticle("Tiny Smoke Ball 1", "Base.rte")
			if Effect then
				Effect.Pos = self.Pos + Vector(0,-2):RadRotate(self.RotAngle)
				Effect.Vel = (self.Vel / 5) - Vector(2*self.negNum,0):RadRotate(self.RotAngle)
				MovableMan:AddParticle(Effect)
			end
		end

		for i = 1, 1 do
			Effect = CreateMOSParticle("Tiny Smoke Ball 1", "Base.rte")
			if Effect then
				Effect.Pos = self.Pos + Vector(0,-4):RadRotate(self.RotAngle)
				Effect.Vel = (self.Vel / 5) - Vector(2*self.negNum,0):RadRotate(self.RotAngle)
				MovableMan:AddParticle(Effect)
			end
		end	
	
		for i = 1, 1 do
			Effect = CreateMOSParticle("Tiny Smoke Ball 1", "Base.rte")
			if Effect then
				Effect.Pos = self.Pos + Vector(0,-6):RadRotate(self.RotAngle)
				Effect.Vel = (self.Vel / 5) - Vector(2*self.negNum,0):RadRotate(self.RotAngle)
				MovableMan:AddParticle(Effect)
			end
		end
	end
	
	
	if self.HFlipped then
		self.negNum = -1;
	else
		self.negNum = 1;
	end
	
	if self:GetNumberValue("Block Mode") == 1 then
	
		self.GibWoundLimit = 60
		
		self.blockedWounds = self.WoundCount - self.lastWounds
	
		actor = MovableMan:GetMOFromID(self.RootID);
		if actor and IsAHuman(actor) then
		
			parent = ToAHuman(actor);
			
			parent:GetController():SetState(Controller.AIM_SHARP,false);		
		
			local dist
			for p in MovableMan.Particles do
				if p.ClassName == "MOPixel" and p.HitsMOs and p.Vel.Magnitude >= 25 and self.blockTimer:IsPastSimMS(200) and p.Team ~= self.Team then
					dist = SceneMan:ShortestDistance(self.Pos , p.Pos,true).Magnitude
					if dist < 25 then
						local angle = SceneMan:ShortestDistance(self.Pos,p.Pos, true).AbsRadAngle
						self.randblock = math.random(-5,5);
						self.BlockAngle = angle - (self.randblock * 0.4 * -1 * self.negNum);
						local rand = math.random(-27,27);
						p.Vel = Vector(p.Vel.Magnitude,rand):RadRotate(parent:GetAimAngle(true))/4;
						p:SetWhichMOToNotHit(parent,-1);
						p.Team = self.Team;
						p.IgnoresTeamHits = true;
						local strikePoint = Vector(0,-1);
						parent:AddAbsForce((p.Vel) * 0.5, strikePoint);
						sfx = CreateAEmitter("Katana Block");
						sfx.Pos = self.Pos;
						MovableMan:AddParticle(sfx);
						self:SetNumberValue("Actively Blocking", 1);
						self.blockingTimer:Reset();
					end
				end
			end
		
			if self.HFlipped then
				self.thing = -1
			else
				self.thing = 1
			end
			
			if self:GetNumberValue("Down Twirl") == 1 then
			
				self.StanceOffset = Vector(12+self.num*3,-14):RadRotate(math.sin(self.num*0.27)*0.7)
			
				rotang = (math.sin(self.num2*0.3)*self.negNum) + (-0.2+math.sin(self.num2*0.3)*1+parent:GetAimAngle(false))*self.negNum+(math.pi*1.17*self.thing)
				
			else
			
				self.StanceOffset = Vector(12+self.num*3,-1):RadRotate(math.sin(self.num*0.27)*0.7)
			
				rotang = (math.sin(self.num2*0.3)*self.negNum) + (-0.2+math.sin(self.num2*0.3)*1+parent:GetAimAngle(false))*self.negNum
	
			end
			
			self.Scale = 1;
			
			
			if self:GetNumberValue("Actively Blocking") == 1 then
			
				self.Scale = 0;
				
				fake = CreateMOSRotating("ScrapperFaction.rte/Katana Fake");	-- doesn't collide with enemies
				fake.Pos = self.Pos;
				fake.Vel = self.Vel;
				--fake.HFlipped = self.HFlipped
				if self.HFlipped then
					fake.RotAngle = rotang-math.pi*1.1;	-- HFlipped doesn't work
				else
					fake.RotAngle = rotang;
				end
				fake.AngularVel = self.AngularVel;
				self:SetNumberValue("AngularVel", fake.AngularVel)
			
				if self.HFlipped then
				
					self:SetNumberValue("RotAngle", fake.RotAngle)
					
				else
				
					self:SetNumberValue("RotAngle", fake.RotAngle)
			
				end
				MovableMan:AddParticle(fake);
			
				if self.twirlTimer:IsPastSimMS(120) then
					if self:GetNumberValue("Down Twirl") == 1 then
						self:SetNumberValue("Down Twirl", 0);
						self:SetNumberValue("Up Twirl", 1);
					else
						self:SetNumberValue("Down Twirl", 1);
						self:SetNumberValue("Up Twirl", 0);
					end
					self.twirlTimer:Reset();
					sfx = CreateAEmitter("Katana Whoosh");
					sfx.Pos = self.Pos;
					MovableMan:AddParticle(sfx);
					self.parryTimer:Reset();
				end
			end
	
			if self.parryTimer:IsPastSimMS(1000) and self:GetNumberValue("Actively Blocking") == 0 then
				self:SetNumberValue("Block Mode", 0);
				self.Scale = 1;
				self.num = 0;
				self.num2 = 0;
				sfx = CreateAEmitter("Katana Whoosh");
				sfx.Pos = self.Pos;
				MovableMan:AddParticle(sfx);
			end
	
			if self.blockingTimer:IsPastSimMS(500) then
				self:SetNumberValue("Actively Blocking", 0);
				self:SetNumberValue("Down Twirl", 1);
				self:SetNumberValue("Up Twirl", 0);
			end
			self:SetNumberValue("RotAngle", self.RotAngle)
			self:SetNumberValue("AngularVel", self.AngularVel)
			
			if self.HFlipped then
				
				self:SetNumberValue("RotAngle", rotang)
					
			else
				
				self:SetNumberValue("RotAngle", rotang)
		
			end
			
			self:Deactivate()
				
			self.RotAngle = rotang;	
					
		end
	end

	
	if self:GetNumberValue("Block Mode") == 0 then
	
		if self.regenTimer:IsPastSimMS(2000) then
			self:RemoveWounds(1);
			self.regenTimer:Reset();
		end
	
		self:RemoveWounds(self.blockedWounds)
		self.blockedWounds = 0;
		
		self.GibWoundLimit = 15;
	
		self.lastWounds = self.WoundCount;
	
		actor = MovableMan:GetMOFromID(self.RootID);
		if actor and IsAHuman(actor) then
		
			parent = ToAHuman(actor);
			
			parent:GetController():SetState(Controller.AIM_SHARP,false);
			
			self.StanceOffset = Vector(12+self.num*3,1):RadRotate(math.sin(self.num*0.3))
			
			local rotang = (math.sin(self.num2*0.3)*self.negNum) + (-0.2+math.sin(self.num2*0.3)*1+parent:GetAimAngle(false))*self.negNum;
							
			self:SetNumberValue("RotAngle", self.RotAngle)
			self:SetNumberValue("AngularVel", self.AngularVel)
				
			if self:IsActivated() and self:GetNumberValue("Striking") == 0 and self:GetNumberValue("Recovery") == 0 and self.recoveryTimer:IsPastSimMS(200) then
			
				self:Deactivate();
				self:SetNumberValue("Striking", 1)
				sfx = CreateAEmitter("Katana Backswing");
				sfx.Pos = self.Pos;
				MovableMan:AddParticle(sfx);
				
			end
			
			if self:IsActivated() then
				self:Deactivate();
			end

			if self:GetNumberValue("Striking") == 1 then
			
				self:SetNumberValue("AngularVel", self.AngularVel)
			
				if self.HFlipped then
				
					self:SetNumberValue("RotAngle", rotang*-1)
					
				else
				
					self:SetNumberValue("RotAngle", rotang)
			
				end
				self.Scale = 0;	-- goes through enemies
				
				local fake

				fake = CreateMOSRotating("ScrapperFaction.rte/Katana Fake");	-- doesn't collide with enemies
				fake.Pos = self.Pos;
				fake.Vel = self.Vel;
				--fake.HFlipped = self.HFlipped
				if self.HFlipped then
					fake.RotAngle = rotang*-1;	-- HFlipped doesn't work
				else
					fake.RotAngle = rotang;
				end
				fake.AngularVel = self.AngularVel;
				self:SetNumberValue("AngularVel", fake.AngularVel)
			
				if self.HFlipped then
				
					self:SetNumberValue("RotAngle", fake.RotAngle)
					
				else
				
					self:SetNumberValue("RotAngle", fake.RotAngle)
			
				end
				MovableMan:AddParticle(fake);
			
				self:Deactivate()
			
				if self.strikeTimerReset == false then
					self.strikeTimer:Reset()
					self.strikeTimerReset = true;
				end
				
				self.RotAngle = rotang;
				
				self.num = self.num + 0.9
				self.num2 = self.num2 + 0.9

				self.lastAngle = parent:GetAimAngle(true);
				
				if self.num > 10 then
					self:Activate()
					self:SetNumberValue("Striked", 1)
					self.effectLowerSpawn = true;
					self.effectSpawn = true;
					self.effectUpperSpawn = true;
				end
				
				if self.strikeTimer:IsPastSimMS(240) then
					self:SetNumberValue("Striking", 0)
					self:SetNumberValue("Recovery", 1)
					self.strikeTimerReset = false;
				end
			end
			
			if self:GetNumberValue("Striked") == 1 then
			
				local Vector2 = (Vector(2,0):GetXFlipped(self.HFlipped)):RadRotate(self.RotAngle)

				self.ray = SceneMan:CastMORay(self.Pos+Vector(0, -8), Vector2, self.RootID, self.Team, 128, false, 2);

				self.rayUpper = SceneMan:CastMORay(self.Pos+Vector(-1, -16), Vector2, self.RootID, self.Team, 128, false, 2);

				self.rayLower = SceneMan:CastMORay(self.Pos+Vector(0, -1), Vector2, self.RootID, self.Team, 128, false, 2);	

				if self.ray > 0 then
				
					if self.effectSpawn == true then
				
						for i = 1, 2 do
							local Effect = CreateMOPixel("Particle Katana", "ScrapperFaction.rte")
							if Effect then
								Effect.Vel = self.Vel + (Vector(70, 0):GetXFlipped(self.HFlipped):RadRotate(self.RotAngle));
								Effect.Pos = self.Pos + (Vector(0, -8):RadRotate(self.RotAngle));
								Effect.Team = self.Team;
								Effect.IgnoresTeamHits = true;
								MovableMan:AddParticle(Effect);
								self.effectSpawn = false;
							end
						end
					end
				end
				
				if self.rayLower > 0 then
				
					if self.effectLowerSpawn == true then
				
						for i = 1, 1 do
							local Effect = CreateMOPixel("Particle Katana", "ScrapperFaction.rte")
							if Effect then
								Effect.Vel = self.Vel + (Vector(70, 0):GetXFlipped(self.HFlipped):RadRotate(self.RotAngle));
								Effect.Pos = self.Pos + (Vector(0, -1):RadRotate(self.RotAngle));
								Effect.Team = self.Team;
								Effect.IgnoresTeamHits = true;
								MovableMan:AddParticle(Effect)
								self.effectLowerSpawn = false
							end
						end
					end
				end
				
				if self.rayUpper > 0 then
				
					if self.effectUpperSpawn == true then
				
						for i = 1, 1 do
							local Effect = CreateMOPixel("Particle Katana", "ScrapperFaction.rte")
							if Effect then
								Effect.Vel = self.Vel + (Vector(70, 0):GetXFlipped(self.HFlipped):RadRotate(self.RotAngle));
								Effect.Pos = self.Pos + (Vector(1, -16):RadRotate(self.RotAngle));
								Effect.Team = self.Team;
								Effect.IgnoresTeamHits = true;
								MovableMan:AddParticle(Effect)
								self.effectUpperSpawn = false
							end
						end
					end
				end
			end
			
			if self:GetNumberValue("Recovery") == 1 then
			
				self:SetNumberValue("Striked", 0);
			
				self.Scale = 1;
			
				self:Deactivate()
				parent:GetController():SetState(Controller.WEAPON_FIRE,false);
			
				self.RotAngle = rotang;
				
				self:SetNumberValue("RotAngle", rotang)
			
				if self.num > 0 then
					self.num = self.num - 0.56;
				elseif self.num < 0 then
					self.num = 0;
				end
				
				if self.num2 > 0 then
					self.num2 = self.num2 - 0.4;
				elseif self.num2 < 0 then
					self.num2 = 0;
				end
		
				if self.num == 0 and self.num2 == 0 then
					self:SetNumberValue("Recovery", 0)
					self.recoveryTimer:Reset();
				end
			end
			
		else
		
			self:SetNumberValue("RotAngle", self.RotAngle)
			self.Scale = 1;
		
		end
	end
		
	if self.FiredFrame and self:GetNumberValue("Fire Upgrade") == 2 then
		sfx = CreateAEmitter("Katana Fire Sound");
		sfx.Pos = self.Pos;
		MovableMan:AddParticle(sfx);
		
		
		for i = 1, 1 do
			Effect = CreateMOSParticle("Explosion Smoke 1")
			if Effect then
				Effect.Pos = self.MuzzlePos + Vector(4*self.negNum,0):RadRotate(self.RotAngle)
				Effect.Vel = (self.Vel + Vector(RangeRand(-30,30), RangeRand(-30,30)) + Vector(50*self.negNum,0):RadRotate(self.RotAngle)) / 25
				Effect.Team = self.Team
				Effect.IgnoresTeamHits = true
				Effect.HitsMOs = false
				MovableMan:AddParticle(Effect)
			end
		end		
		for i = 1, 3 do
			Effect = CreateMOSParticle("Tiny Smoke Ball 1", "Base.rte")
			if Effect then
				Effect.Pos = self.MuzzlePos + Vector(4*self.negNum,0):RadRotate(self.RotAngle)
				Effect.Vel = (self.Vel + Vector(RangeRand(-30,30), RangeRand(-30,30)) + Vector(50*self.negNum,0):RadRotate(self.RotAngle)) / 30
				MovableMan:AddParticle(Effect)
			end
		end

		for i = 1, 3 do
			Effect = CreateMOSParticle("Tiny Smoke Ball 1", "Base.rte")
			if Effect then
				Effect.Pos = self.MuzzlePos + Vector(4*self.negNum,0):RadRotate(self.RotAngle)
				Effect.Vel = (self.Vel + Vector(RangeRand(-30,40), RangeRand(-30,30)) + Vector(50*self.negNum,0):RadRotate(self.RotAngle)) / 1
				MovableMan:AddParticle(Effect)
			end
		end

		for i = 1, 6 do
			Effect = CreateMOSParticle("Particle Katana Flame")
			if Effect then
				Effect.Pos = self.MuzzlePos + Vector(4*self.negNum,0):RadRotate(self.RotAngle)
				Effect.Vel = (self.Vel + Vector(RangeRand(-1,1), RangeRand(-1,1)) + Vector(10*self.negNum,0):RadRotate(self.RotAngle)) / 1
				Effect.Team = self.Team
				MovableMan:AddParticle(Effect)
			end
		end
	end
	
	if parent then
	
		if parent:GetController():IsState(Controller.WEAPON_RELOAD) and self.changedMode ~= true then
			if self:GetNumberValue("Block Mode") == 0 then
				self:SetNumberValue("Block Mode", 1);
				self.parryTimer:Reset();
			else
				self.Scale = 1;
				self:SetNumberValue("Block Mode", 0);
			end
			self.changedMode = true;
			sfx = CreateAEmitter("Katana Whoosh");
			sfx.Pos = self.Pos;
			MovableMan:AddParticle(sfx);
			self:SetNumberValue("HaveToResetNum", 1)
		else
			self.changedMode = false;
		end
	end
end