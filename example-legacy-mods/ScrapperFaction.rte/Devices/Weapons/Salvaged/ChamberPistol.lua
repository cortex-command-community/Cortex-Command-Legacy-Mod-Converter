
function Create(self)

	self.parent = nil;
	self.pullTimer = Timer();

	self.newMag = false;
	self.chamber = true;
	self.num = math.pi;
	self.sfx = true;
	self.casing = false;

	self.negNum = 0;

	self.sLength = self.SharpLength;

	if self.Magazine then
		self.lastAmmo = self.Magazine.RoundCount;
	end

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
	end

	if self.HFlipped then
		self.negNum = -1;
	else
		self.negNum = 1;
	end

	if self.parent then

		if self.Magazine then

			if self.newMag == true then

				self.chamber = true;	-- pull bolt on new mag
				self.pullTimer:Reset();
				self.num = math.pi;
				self.sfx = true;

				self.newMag = false;

			elseif self.Magazine.RoundCount < self.lastAmmo then--and self.chamber == false then

				self.chamber = true;	-- pull bolt after firing
				self.pullTimer:Reset();
				self.num = math.pi;
				self.sfx = true;
				self.casing = true;
			end

			self.lastAmmo = self.Magazine.RoundCount;

			if self.Magazine.RoundCount == 0 and self:IsActivated() then
				self:Reload();
			end
		else
			self.newMag = true;
		end

		if self.chamber == true then	-- pulling the bolt

			--self:Deactivate();
			--self.parent:GetController():SetState(Controller.WEAPON_FIRE,false);

			if self.pullTimer:IsPastSimMS(300) then
				--self.parent:GetController():SetState(Controller.AIM_SHARP,false);
				--self.Frame = 1;

				if self.sfx ~= false then
					sfx = CreateAEmitter("Chamber Salvaged Pistol");
					sfx.Pos = self.Pos;
					MovableMan:AddParticle(sfx);

					self.sfx = false;
				end

				if self.casing == true then
					casing = CreateMOSParticle("Casing");
					casing.Pos = self.Pos+Vector(-4*self.negNum,-1):RadRotate(self.RotAngle);
					casing.Vel = self.Vel+Vector(-math.random(1,1)*self.negNum,-math.random(1,1)):RadRotate(self.RotAngle);
					MovableMan:AddParticle(casing);

					self.casing = false;
				end

				self.SharpLength = self.SharpLength+(self.sLength/30)*math.sin(2*self.num);

				self.RotAngle = self.RotAngle +self.negNum*math.sin(self.num)/2;

				self.num = self.num - math.pi*0.05;
			end

			if self.num <= 0 then

				self.num = 0;
				self.chamber = false;
				self.SharpLength = self.sLength;
			end
		end
	end
end