function Create(self)

	self.moveSoundTimer = Timer()

end

function Update(self)

	-- get parent
	local parent;
	local actor = MovableMan:GetMOFromID(self.RootID);
	if actor and IsAHuman(actor) then
		
		parent = ToAHuman(actor);
		self.parent = ToAHuman(actor);
		
		if parent:GetController():IsState(Controller.MOVE_LEFT) or parent:GetController():IsState(Controller.MOVE_RIGHT) then
		
			--script for making sounds on movement, up: check for left or right presses, down: use a timer to make sounds every 800ms

			if self.moveSoundTimer:IsPastSimMS(800) then
				local sfx = CreateAEmitter("Shield Move");
				sfx.Pos = self.Pos;
				MovableMan:AddParticle(sfx);
				self.moveSoundTimer:Reset();
			end
		end		
	end
end