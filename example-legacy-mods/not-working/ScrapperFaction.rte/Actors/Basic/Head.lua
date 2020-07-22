function Create(self)

	self.negNum = 1;
	self.negAng = 0;
	if self.HFlipped then
		self.negNum = -1;
		self.negAng = 3.14;	--pi
	end

	local selfPosX = self.Pos.X;	-- trying to avoid crashes
	local selfPosY = self.Pos.Y;

	self.head = math.random(8)-1;
	self.Frame = self.head;
	if not string.find(self.PresetName, "Bruiser") then -- bruisers and snipers doesn't have dynamic hair
		if self.head == 2 or self.head == 6 then		-- mia
			self.hair = CreateMOSRotating("ScrapperFaction.rte/Scrappers Hair A");
			self.hairOffset = Vector(-1,-1);
		elseif self.head == 3 or self.head == 7 then	-- sandra
			self.hair = CreateMOSRotating("ScrapperFaction.rte/Scrappers Ponytail A");
			self.hairOffset = Vector(-4,-3);
		end
		if self.hair then
			self.hair.Vel = Vector(0,0);
			self.hair.AngularVel = 0;

			self.hair.Pos = Vector(selfPosX, selfPosY) + Vector(self.hairOffset.X*self.negNum, self.hairOffset.Y):RadRotate(self.RotAngle);
			self.hair.HFlipped = self.HFlipped;
			local rot = Vector(self.Vel.X-SceneMan.GlobalAcc.X/2, self.Vel.Y-SceneMan.GlobalAcc.Y/2);
			self.hair.RotAngle = rot.AbsRadAngle + self.negAng;

			self.hair.ToSettle = false;
			MovableMan:AddParticle(self.hair);
		end
	end
	self.playerControlled = false;
end

function Update(self)

	self.negNum = 1;
	self.negAng = 0;
	if self.HFlipped then
		self.negNum = -1;
		self.negAng = 3.14;	--pi
	end
	local selfPosX = self.Pos.X;	-- trying to avoid crashes
	local selfPosY = self.Pos.Y;

	if self.hair
	and self.ToDelete == false
	and self.hair.ToDelete == false then
		self.hair.Vel = Vector(0,0);
		self.hair.AngularVel = 0;

		self.hair.Pos = Vector(selfPosX, selfPosY) + Vector(self.hairOffset.X*self.negNum, self.hairOffset.Y):RadRotate(self.RotAngle);
		self.hair.HFlipped = self.HFlipped;
		local rot = Vector(self.Vel.X-SceneMan.GlobalAcc.X/2, self.Vel.Y-SceneMan.GlobalAcc.Y/2);
		self.hair.RotAngle = rot.AbsRadAngle + self.negAng;

		if rot.Magnitude < 6 then	--5?
			self.hair.Frame = 1;
		else
			self.hair.Frame = 0;
		end

		self.hair.ToSettle = false;	-- fucking don't settle please
	end

	actor = MovableMan:GetMOFromID(self.RootID);
	if actor and IsAHuman(actor) then
		actor = ToAHuman(actor);
		if actor:GetController():IsState(Controller.WEAPON_FIRE) or actor.Health < 50 then
			self.Frame = self.head + 8;
		else
			self.Frame = self.head;
		end

		if not actor:IsPlayerControlled() then -- and actor.AIMode == Actor.AIMODE_SENTRY then
			
			if actor:GetNumberValue("Body State") == 1 then	-- 0 = neutral, 1 = crouch, 2 = stand

				if actor:GetController():IsState(Controller.BODY_JUMPSTART)
				or actor:GetController():IsState(Controller.BODY_JUMP) then
					actor:GetController():SetState(Controller.BODY_CROUCH,false);	-- stand up if using jetpack(?)
				else
					actor:GetController():SetState(Controller.BODY_CROUCH,true);
				end

				if self.playerControlled == true then

					if self.HFlipped then
						actor:GetController():SetState(Controller.MOVE_LEFT,true);	-- go prone
						actor.Vel = actor.Vel + Vector(3,-1);
					else
						actor:GetController():SetState(Controller.MOVE_RIGHT,true);
						actor.Vel = actor.Vel + Vector(-3,-1);
					end
					self.playerControlled = false;
				end

			elseif actor:GetNumberValue("Body State") == 2 then

				actor:GetController():SetState(Controller.BODY_CROUCH,false)
			end
		else
			self.playerControlled = true;
		end
	end
end