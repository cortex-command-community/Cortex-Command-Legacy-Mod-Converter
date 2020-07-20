function Create(self)

	self.checks = 5;
	self.checkdist =	math.sqrt(
				FrameMan.PlayerScreenHeight^2
				+FrameMan.PlayerScreenWidth^2
				)/self.checks;	
	self.target = nil;
end

function Update(self)

	if self.target then

		local dist =	self.target.Pos-self.Pos;

		if dist.Magnitude < 25 then

			ActivityMan:GetActivity():SetTeamFunds(ActivityMan:GetActivity():GetTeamFunds(self.target.Team) + 10, self.target.Team);

			part = CreateMOPixel("4Z.rte/Gold Flash");
			part.Pos = self.target.Pos;
			MovableMan:AddParticle(part);

			self.ToDelete = true;
		else

			local speed =	70 / (math.sqrt(dist.Magnitude)+1)

			self.Pos = self.Pos+(dist:SetMagnitude(speed));
		end
	else
		for actor in MovableMan.Actors do

			if actor.Team == 0 then

				for i = 1, self.checks do

					local target
					local checkPos = SceneMan:ShortestDistance(self.Pos, actor.Pos, true);

					if checkPos.Magnitude < self.checkdist*i then		-- this is a crude system but idc
												-- jus try to find the closest act
						self.target = ToActor(actor);
						break;
					end
				end

				--if self.target == nil then				-- if not close enough just pick one

				--	self.target = ToActor(actor);
				--	break;
				--end
			end
		end
	end
end