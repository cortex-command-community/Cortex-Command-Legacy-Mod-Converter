function Create(self)
	self.Defense = 100;
	self.lifeTimer = Timer();
	
	self.LastHealth = self.Health;
	self.Alternate = true;
	self.Counter = 0;
end

function Update(self)
	if self.lifeTimer:IsPastSimMS(5000) then
		self:GibThis();
	end

	if self.Health < self.LastHealth then
		local diff = self.LastHealth - self.Health;
		for i = 1, diff do
			self.Counter = self.Counter + 1;
			if self.Counter == self.Defense then
				self.Counter = 0;
			else
				self.Health = self.Health + 1;
			end
		end
	end
	self.LastHealth = self.Health;
end
