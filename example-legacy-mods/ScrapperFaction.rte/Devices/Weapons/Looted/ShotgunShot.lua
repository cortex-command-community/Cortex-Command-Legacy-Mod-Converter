
	-- this script randomly weakens the shot particle to diminish power in long range --

function Create(self)
	self.time = math.random(50,100);
	self.timer = Timer();
end

function Update(self)

	if self.timer:IsPastSimMS(self.time) then
		self.timer:Reset();

		self.Mass = self.Mass*0.9;		--
		self.Sharpness = self.Sharpness*0.9;	-- drop sharpness and mass by 10%
	end
end