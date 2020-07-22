
function Create(self)

	self.parent = nil;
	self.pullTimer = Timer();

	self.newMag = false;
	self.chamber = true;		--
	--self.pullTimer:Reset();	--
	self.num = math.pi;		--
	self.sfx = true;		--
	self.sfxSetShot = true;
	self.sfxSetTail = true;
	self.sfxSetMech = true;

	self.negNum = 0;
	self.sLength = self.SharpLength;
	self.ShakeRange = 6
	self.sRange = self.ShakeRange
	self.lifeTimer = Timer();
	self.lifeTimerReset = false
	self.flashCooldown = Timer();
	self.flashedTimer = Timer();
	self.shotTimer = Timer();

	local actor = MovableMan:GetMOFromID(self.RootID);
	if actor and IsAHuman(actor) then
		self.parent = ToAHuman(actor);
	end
end

function Update(self)

	local actor = MovableMan:GetMOFromID(self.RootID);
	if actor and IsAHuman(actor) then
		self.parent = ToAHuman(actor);
	else
		self.parent = nil;
	-- cock and load on pickup
		--self.chamber = true;	--
		--self.pullTimer:Reset();	--
		--self.num = math.pi;	--
		--self.sfx = true;	--
	end

	if self.justShot == true then
	
		if self.shotTimer:IsPastSimMS(50) then
		
			if self.echoMakingSound == true then
				
				if MovableMan:IsParticle(self.echoSound) then	

					self.echoSound.ToDelete = true;
				
					self.echoMakingSound = false;		
		

				end
			
			end
		
			self.justShotTail = true;
			
			for i = 1, 2 do
				Effect = CreateMOSParticle("Tiny Smoke Ball 1", "Base.rte")
				if Effect then
					Effect.Pos = self.MuzzlePos;
					Effect.Vel = (self.Vel + Vector(RangeRand(-20,20), RangeRand(-20,20)) + Vector(150*self.negNum,0):RadRotate(self.RotAngle)) / 30
					MovableMan:AddParticle(Effect)
				end
			end
			
			if PosRand() < 0.5 then
				Effect = CreateMOSParticle("Side Thruster Blast Ball 1", "Base.rte")
				if Effect then
					Effect.Pos = self.MuzzlePos;
					Effect.Vel = (self.Vel + Vector(150*self.negNum,0):RadRotate(self.RotAngle)) / 10
					MovableMan:AddParticle(Effect)
				end
			end
			
			if self.ray < 0 or self.rayRight < 0 or self.rayLeft < 0 then
			
				if self.sfxSetMech ~= false then

					sfxSetShot = CreateAEmitter("Add Custom HBR");
					sfxSetShot.Pos = self.Pos;
					MovableMan:AddParticle(sfxSetShot);

				end
			else
	
				-- if self.sfxSetShot ~= false then

					-- sfxSetShot = CreateAEmitter("Noise Custom HBR");
					-- sfxSetShot.Pos = self.Pos;
					-- MovableMan:AddParticle(sfxSetShot);

				-- end
				
				if self.sfxSetMech ~= false then

					sfxSetShot = CreateAEmitter("AddShort Custom HBR");
					sfxSetShot.Pos = self.Pos;
					MovableMan:AddParticle(sfxSetShot);

				end
			end
			
			if self.sfxSetShot ~= false then

				sfxSetShot = CreateAEmitter("Rattle Custom HBR");
				sfxSetShot.Pos = self.Pos;
				MovableMan:AddParticle(sfxSetShot);

			end

			if self.sfxSetMech ~= false then

				sfxSetShot = CreateAEmitter("HiFi Custom HBR");
				sfxSetShot.Pos = self.Pos;
				MovableMan:AddParticle(sfxSetShot);

			end
			
			if self.sfxSetMech ~= false then

				sfxSetShot = CreateAEmitter("Shell Custom HBR");
				sfxSetShot.Pos = self.Pos;
				MovableMan:AddParticle(sfxSetShot);

			end
			
			if self.sfxSetMech ~= false then

				sfxSetShot = CreateAEmitter("CoreBass Custom HBR");
				sfxSetShot.Pos = self.Pos;
				MovableMan:AddParticle(sfxSetShot);

			end
			
			self.justShot = false;
		end
		
	end
	
	if not self:IsActivated() then

		if self.justShotTail == true then
		
			if self.parent then
			
				if self.parent:IsPlayerControlled() then
					self.justShotTail = false;

					if self.ray < 0 or self.rayRight < 0 or self.rayLeft < 0 then

						if self.sfxSetTail ~= false then

							self.sfx = CreateAEmitter("Reflection Custom HBR");
							self.sfx.Pos = self.Pos;
							self.echoSound = ToAEmitter(self.sfx)
							MovableMan:AddParticle(self.sfx);
							self.echoMakingSound = true;
							

						end
					else
						if self.ray > 200 or self.rayRight > 200 or self.rayLeft > 200 then					
				
							if self.sfxSetTail ~= false then

								self.sfx = CreateAEmitter("Reflection Big Custom HBR Indoors");
								self.sfx.Pos = self.Pos;
								self.echoSound = ToAEmitter(self.sfx)
								MovableMan:AddParticle(self.sfx);
								self.echoMakingSound = true;

							end
						else
							if self.sfxSetTail ~= false then

								self.sfx = CreateAEmitter("Reflection Custom HBR Indoors");
								self.sfx.Pos = self.Pos;
								self.echoSound = ToAEmitter(self.sfx)
								MovableMan:AddParticle(self.sfx);
								self.echoMakingSound = true;

							end			
						end
					end
				else
					self.justShotTail = false;

					if self.ray < 0 or self.rayRight < 0 or self.rayLeft < 0 then

						if self.sfxSetTail ~= false then

							self.sfx = CreateAEmitter("Reflection Weak Custom HBR");
							self.sfx.Pos = self.Pos;
							self.echoSound = ToAEmitter(self.sfx)
							MovableMan:AddParticle(self.sfx);
							self.echoMakingSound = true;
							

						end
					else
						if self.ray > 200 or self.rayRight > 200 or self.rayLeft > 200 then					
				
							if self.sfxSetTail ~= false then

								self.sfx = CreateAEmitter("Reflection Big Weak Custom HBR Indoors");
								self.sfx.Pos = self.Pos;
								self.echoSound = ToAEmitter(self.sfx)
								MovableMan:AddParticle(self.sfx);
								self.echoMakingSound = true;

							end
						else
							if self.sfxSetTail ~= false then

								self.sfx = CreateAEmitter("Reflection Weak Custom HBR Indoors");
								self.sfx.Pos = self.Pos;
								self.echoSound = ToAEmitter(self.sfx)
								MovableMan:AddParticle(self.sfx);
								self.echoMakingSound = true;

							end			
						end
					end
				end
			end
		end	
	end
		

	if self.FiredFrame then	
	

		self.justShot = true;
		self.shotTimer:Reset();
		
		if self.sfxSetShot ~= false then

			sfxSetShot = CreateAEmitter("Pre Custom HBR");
			sfxSetShot.Pos = self.Pos;
			MovableMan:AddParticle(sfxSetShot);

		end

		local Vector2 = Vector(0,-700);

		local Vector2Left = Vector(0,-700):RadRotate(45);

		local Vector2Right = Vector(0,-700):RadRotate(-45);

		local Vector3 = Vector(0,0);

		local Vector4 = Vector(0,0);

		self.ray = SceneMan:CastObstacleRay(self.Pos, Vector2, Vector3, Vector4, self.RootID, self.Team, 128, 7);

		self.rayRight = SceneMan:CastObstacleRay(self.Pos, Vector2Right, Vector3, Vector4, self.RootID, self.Team, 128, 7);

		self.rayLeft = SceneMan:CastObstacleRay(self.Pos, Vector2Left, Vector3, Vector4, self.RootID, self.Team, 128, 7);

		if self.ray < 0 or self.rayRight < 0 or self.rayLeft < 0 then					
			
		else
	
		end

	end

	if self:DoneReloading() == true and self.lastMagazineAmmo > 0 then
		self.Magazine.RoundCount = self.Magazine.RoundCount + 1;
		self.newMag = false;
	end

	if self.HFlipped then
		self.negNum = -1;
	else
		self.negNum = 1;
	end

	if self.parent == nil and self.chamber == true then
		
		self.chamber = false;
		if self.pullTimer:IsPastSimMS(450) then
		
		
		else
			self.stoppedPremature = true;
		end
		self:RemoveNumberValue("ChamberRot")
		self:RemoveNumberValue("Chambering")

	end
	if self.parent then	

		
		if self.Magazine then
		
			if self.stoppedPremature == true then
				
				self.chamber = true;
				self.pullTimer:Reset();
				self.num = math.pi;
				self.sfx = true;

				self.stoppedPremature = false;
			end


			self.lastAmmo = self.Magazine.RoundCount;

			if self.newMag == true then

				self.chamber = true;
				self.pullTimer:Reset();
				self.num = math.pi;
				self.sfx = true;

				self.newMag = false;
			end
			self.lastMag = self.Magazine;
			self.velApplied = false;
		else
			
			self.newMag = true;
			self.lastMagazineAmmo = self.lastAmmo;
			
			if self.justShotTail == true then
			
				if self.parent then
				
					if self.parent:IsPlayerControlled() then
						self.justShotTail = false;

						if self.ray < 0 or self.rayRight < 0 or self.rayLeft < 0 then

							if self.sfxSetTail ~= false then

								self.sfx = CreateAEmitter("Reflection Custom HBR");
								self.sfx.Pos = self.Pos;
								self.echoSound = ToAEmitter(self.sfx)
								MovableMan:AddParticle(self.sfx);
								self.echoMakingSound = true;
								

							end
						else
							if self.ray > 200 or self.rayRight > 200 or self.rayLeft > 200 then					
					
								if self.sfxSetTail ~= false then

									self.sfx = CreateAEmitter("Reflection Big Custom HBR Indoors");
									self.sfx.Pos = self.Pos;
									self.echoSound = ToAEmitter(self.sfx)
									MovableMan:AddParticle(self.sfx);
									self.echoMakingSound = true;

								end
							else
								if self.sfxSetTail ~= false then

									self.sfx = CreateAEmitter("Reflection Custom HBR Indoors");
									self.sfx.Pos = self.Pos;
									self.echoSound = ToAEmitter(self.sfx)
									MovableMan:AddParticle(self.sfx);
									self.echoMakingSound = true;

								end			
							end
						end
					else
						self.justShotTail = false;

						if self.ray < 0 or self.rayRight < 0 or self.rayLeft < 0 then

							if self.sfxSetTail ~= false then

								self.sfx = CreateAEmitter("Reflection Weak Custom HBR");
								self.sfx.Pos = self.Pos;
								self.echoSound = ToAEmitter(self.sfx)
								MovableMan:AddParticle(self.sfx);
								self.echoMakingSound = true;
								

							end
						else
							if self.ray > 200 or self.rayRight > 200 or self.rayLeft > 200 then					
					
								if self.sfxSetTail ~= false then

									self.sfx = CreateAEmitter("Reflection Big Weak Custom HBR Indoors");
									self.sfx.Pos = self.Pos;
									self.echoSound = ToAEmitter(self.sfx)
									MovableMan:AddParticle(self.sfx);
									self.echoMakingSound = true;

								end
							else
								if self.sfxSetTail ~= false then

									self.sfx = CreateAEmitter("Reflection Weak Custom HBR Indoors");
									self.sfx.Pos = self.Pos;
									self.echoSound = ToAEmitter(self.sfx)
									MovableMan:AddParticle(self.sfx);
									self.echoMakingSound = true;

								end			
							end
						end
					end
				end
			end	
		end

		if self.chamber == true then
			self:SetNumberValue("ChamberRot", self.RotAngle)
			self:SetNumberValue("Chambering", 1)
			self:Deactivate();
			--self.parent:GetController():SetState(Controller.WEAPON_FIRE,false);

			if self.pullTimer:IsPastSimMS(550) then
				--self.parent:GetController():SetState(Controller.AIM_SHARP,false);
				--self.Frame = 1;

				if self.sfx ~= false then
					sfx = CreateAEmitter("Chamber " .. self.PresetName);
					sfx.Pos = self.Pos;
					MovableMan:AddParticle(sfx);

					self.sfx = false;
				end

				self.RotAngle = self.RotAngle +self.negNum*math.sin(self.num)/8;

				self:SetNumberValue("ChamberRot", self.RotAngle)

				self.num = self.num - math.pi*0.060;
			end

			if self.num <= 0 then

				self.num = 0;
				self.chamber = false;
				self.ShakeRange = self.sRange
				self:RemoveNumberValue("Chambering")
			end
		end
	end
end