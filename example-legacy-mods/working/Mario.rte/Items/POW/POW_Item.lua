function Create(self)
	self.throwSpeed = 1;	-- Base speed
	--if self.Magazine then	self.throwSpeed = self.Magazine.NextRound.FireVel;	end
end

function Update(self)
	local parent = MovableMan:GetMOFromID(self.RootID);
	if parent and IsActor(parent) then
		self.RotAngle = self.RotAngle * 0.3;
		self.Pos.Y = self.Pos.Y - 8;
		parent = ToActor(parent);
		local negNum = 1;
		if parent.HFlipped then
			negNum = -1;
		end
		local arm = self:GetParent();
		local ctrl = parent:GetController();
		local throwVec = Vector(self.throwSpeed + math.sqrt(arm.Mass + arm.Radius + arm.Material.StructuralIntegrity) * negNum, 0):RadRotate(parent:GetAimAngle(false) * 0.6 * negNum);
		if ctrl:IsState(Controller.AIM_SHARP) then
			ctrl:SetState(Controller.AIM_SHARP, false);
			local arrow = CreateMOSRotating("Mario.rte/Guide Arrow");
			local guidepos = self.Pos + Vector(throwVec.X, throwVec.Y):SetMagnitude((throwVec.Magnitude + parent.AimDistance) / 2);
			FrameMan:DrawBitmapPrimitive(ctrl.Player, guidepos, arrow, throwVec.AbsRadAngle, 0);
		end
		if self.FiredFrame then
			self.StanceOffset = Vector(arm.Diameter, 5);
			local block = CreateMOSRotating("Mario.rte/POW Block");
			block.Pos = self.Pos;
			block.Vel = parent.Vel / 2 + throwVec;
			block.Team = self.Team;
			block.IgnoresTeamHits = true;
			MovableMan:AddParticle(block);
			parent.AngularVel = parent.AngularVel / 2 + (parent:GetAimAngle(false) - 1.57) * 4 * negNum / (1 + math.abs(parent.RotAngle));
			self.ToDelete = true;
		else
			self.StanceOffset = Vector(5, -arm.Diameter):RadRotate(self.RotAngle * negNum - parent:GetAimAngle(false));
		end
	end
	self.HFlipped = false;
end