
dofile("Base.rte/Constants.lua")
require("Actors/AI/NativeHumanAI")  --dofile("ScrapperFaction.rte/Actors/Basic/MeleeAI/NativeHumanAI.lua")

function Create(self)
	self.AI = NativeHumanAI:Create(self)

	self.settleTimer = Timer();
	self.dead = false;
	self.delay = 5000;		-- base time (in MS) until the body turns into terrain
					-- (+ 100*mass)
					-- basic coalition soldier is about 125 mass (with all limbs attached)

					--> coalition soldier settle time = 5 + 12.5 = 17.5 seconds

	self.tilt = 0.3;	-- for visible inventory

	self.visibleInventory = false;	--
	self.lingeringCorpses = false;	-- change into true to enable
end

function Update(self)

	-- visible inventory starts here --

	if self.visibleInventory then--
	if self.Health > 0 then

		if self:IsInventoryEmpty() == false then

			local a = 0;	-- HDFirearm / HeldDevice
			local b = 0;	-- TDExplosive

			for i = 1, self.InventorySize do

				local item = self:Inventory();
				if item then

					local negNum = 1;
					local fixNum = 0;	-- slightly different offset when flipped

					if self.HFlipped == true then
						negNum = -1;
						fixNum = -1;	-- (negNum-1)*0.5
					end

					if item.ClassName == "TDExplosive" then

						b = b+1;	-- explosives aren't visible as of now but counted anyway for some reason
							
					elseif item.ClassName == "HDFirearm" or item.ClassName == "HeldDevice" then

						a = a+1;

						local fake
						local hdevice = 1;	-- false

						if item.ClassName == "HDFirearm" then
							fake = CreateHDFirearm(item:GetModuleAndPresetName());
						elseif item.ClassName == "HeldDevice" then
							hdevice = 0;
							fake = CreateHeldDevice(item:GetModuleAndPresetName());
						end
						if fake then	-- in case PresetName was changed

							local sRad = math.sqrt(self.Radius);	-- math
							local fRad = math.sqrt(fake.Radius);
							local fmass = math.sqrt(math.abs(fake.Mass));

							fixNum = fixNum+fake.Radius*0.2+math.sqrt(a);	-- math

								-- bigger actors carry weapons higher up
								-- smaller weapons are carried lower down

			fake.Pos = self.Pos+Vector((-sRad-fixNum)*negNum, - sRad -fmass + 1 + hdevice*3):RadRotate(self.RotAngle);	-- math

							local c = math.sqrt(math.abs(self.InventorySize-b));	-- math
							local d = math.sqrt(a);

				-- parent + 90 deg * shieldvar 		- ( wepnum + invsize/2 - shieldvar/mass ) * flip

			fake.RotAngle = self.RotAngle + (math.pi*0.5)*hdevice + (a*self.tilt-c*self.tilt+hdevice/fmass)/c*negNum;	-- math
			--fake.RotAngle = self.RotAngle + (math.pi*0.5)*hdevice - ((d-c-hdevice/fmass)/c)*negNum;	-- math

							--fake.HFlipped = self.HFlipped;	-- HFlipped isn't applied on first frame for some reason
							fake.PinStrength = 100;

							fake.GibImpulseLimit = 0;	-- not sure if these are needed but whatever
							fake.Mass = 1;			--

							fake.Lifetime = 1;	-- one frame

							fake.GetsHitByMOs = false;
							--fake.HitsMOs = true;

							fake.Team = self.Team;
							fake.IgnoresTeamHits = true;

							fake.HUDVisible = false;

							if fake.Magazine then
								fake.Magazine.Scale = 0;	-- prevent phantom magazines at Vector(0,0)
								--fake.Magazine.ToDelete = true;	--
							end

							--fake.PresetName = (fake.PresetName .. i);	-- debug
							MovableMan:AddParticle(fake);
						end
					end

					self:SwapNextInventory(item,true);
				end
			end
		end
	end
	end--
	-- visible inventory ends here --

	-- lingering corpse starts here --

	if self.lingeringCorpses then--
	if self.Health <= 0 and self.Head then
		if self.dead == false then
			self.AngularVel = self.AngularVel-self.Vel.X*math.sqrt(self.Vel.Magnitude);	--
			self.dead = true;
		end
		if not self.settleTimer:IsPastSimMS(self.delay+(100*math.ceil(math.abs(self.Mass)))) then	-- emphasis of actor mass can be changed
			self.Status = 3;
			self.ToSettle = false;
			self.HUDVisible = false;

		--else
		--	self.Status = 4;	-- not exactl
		--	self.ToSettle = true;	-- y required
		end

		-- try to force some non-movement

		self.HFlipped = self.flippedOnDeath;

		self:GetController():SetState(Controller.BODY_JUMP,false);
		self:GetController():SetState(Controller.BODY_JUMPSTART,false);
		self:GetController():SetState(Controller.BODY_CROUCH,false);
		self:GetController():SetState(Controller.PIE_MENU_ACTIVE,false);
		self:GetController():SetState(Controller.WEAPON_FIRE,false);
		self:GetController():SetState(Controller.AIM_SHARP,false);
		self:GetController():SetState(Controller.MOVE_RIGHT,false);
		self:GetController():SetState(Controller.MOVE_LEFT,false);
	else
		self.settleTimer:Reset();
		self.flippedOnDeath = self.HFlipped;
	end
	end--
end

function UpdateAI(self)
	self.AI:Update(self)
end

function Destroy(self)
	self.AI:Destroy(self)
end
