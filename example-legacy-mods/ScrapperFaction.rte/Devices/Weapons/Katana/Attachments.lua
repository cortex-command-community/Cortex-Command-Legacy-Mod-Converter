function Create(self)
	self.Frame = 0;
	self.parent = nil;
	self.num = math.pi;		--
	self.pullTimer = Timer();
	self.timerReset = false
	self.parentIdentified = false

	self.negNum = 0;
end

function Update(self)
	
	if self.parent == nil and self.parentIdentified == false then   -- if self.parent isn't defined

		self.mo = MovableMan:GetMOFromID(self.RootID);
		if self.mo then
			if IsHDFirearm(self.mo) then   -- if root ID is the gun
				self.parent = ToHDFirearm(self.mo);
				self.parentIdentified = true
			elseif IsAHuman(self.mo) then   -- if root ID is the actor holding the gun
				if ToAHuman(self.mo).EquippedItem and IsHDFirearm(ToAHuman(self.mo).EquippedItem) then
					self.parent = ToHDFirearm(ToAHuman(self.mo).EquippedItem);
					self.parentIdentified = true
				end
			end
		end
	elseif IsHDFirearm(self.parent) then
		self.GetsHitByMOs = false
		self.AngularVel = self.parent:GetNumberValue("AngularVel");
		
		if self.parent:NumberValueExists("RotAngle") then	
		
			self.RotAngle = self.parent:GetNumberValue("RotAngle");
			
		end
		if self.parent:GetNumberValue("Fire Upgrade") == 1 then
			self.Frame = 0
		elseif self.parent:GetNumberValue("Fire Upgrade") == 2 then
			self.Frame = 1
		end
	end
	if self.parentIdentified == true and IsHDFirearm(self.parent) == false then
		self.ToDelete = true;
	end
end



