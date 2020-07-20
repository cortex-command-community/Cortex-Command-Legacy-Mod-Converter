function Create(self)
	self.speed = 10;
end
function Update(self)
	self.Vel = Vector(self.Vel.X, self.Vel.Y):SetMagnitude(self.speed);
end