-- this sends actors flying from the blast (4zK)
function Create(self)

	self.strength = 3;	-- variable

	-- whatever part this script is assigned to is expected to not have mass > 0
	-- mass is a vital part in defining the strength of the blast

	self.initPosX = self.Pos.X;
	self.initPosY = self.Pos.Y;

	local lifeFrames = self.Lifetime / 16.67;
	self.range = self.Vel.Magnitude*math.sqrt(lifeFrames+1)*(1-self.AirResistance/60); -- 

	self.terrPass = math.random(20,60);	-- amount of StructualIntegrity the blast can pass (between 20 and 40)

	local c = math.sqrt(self.Mass +1);	-- blast particle mass variable

	if self.Mass > 0 and self.HitsMOs == true then

		-- 1 frame ~= 16.67 MS (?)
		-- lifetime / deltatime = frames alive

		for actor in MovableMan.Actors do

			if self.Team < 0 or actor.Team ~= self.Team then	-- -1 implies everything is affected

				local dist = SceneMan:ShortestDistance(self.Pos,actor.Pos,SceneMan.SceneWrapsX);

				if actor and dist.Magnitude < self.range then

					strCheck = SceneMan:CastStrengthRay(self.Pos, actor.Pos-self.Pos, self.terrPass, Vector(), 3, 0, SceneMan.SceneWrapsX)
					if not(strCheck) then						--snow=18 flesh=30

						local forceVector =	dist:SetMagnitude(
									math.sqrt(self.Vel.Magnitude*self.strength)
									/math.sqrt(dist.Magnitude+1)
									);

				-- actor mass variable
						local a = math.sqrt	(math.abs(actor.Mass)	*0.1 +1 );	-- 10 %
				-- actor vel variable
						local b = math.sqrt	(actor.Vel.Magnitude	*0.4 +1 );	-- 40 %
				-- part mass variable
						--local c = math.sqrt	(self.Mass +1);	-- defined previously

						actor.Vel =	actor.Vel + forceVector / ( (a + b) / c +1 );

						actor.AngularVel = -actor.Vel.X/a;	-- huehuehue

						self.strength = self.strength*0.99;	-- decrease individual strength on every object affected
					end
				end	
			end
		end

		for item in MovableMan.Items do

			if self.Team < 0 or item.Team ~= self.Team then

				local dist = SceneMan:ShortestDistance(self.Pos,item.Pos,SceneMan.SceneWrapsX);

				if item and dist.Magnitude < self.range then

					strCheck = SceneMan:CastStrengthRay(self.Pos, self.Pos-item.Pos, self.terrPass, Vector(), 2, 0, SceneMan.SceneWrapsX)
					if not(strCheck) then

						local forceVector =	dist:SetMagnitude(
									math.sqrt(self.Vel.Magnitude*self.strength)
									/math.sqrt(dist.Magnitude+1)
									);

				-- item mass variable
						local a = math.sqrt	(math.abs(item.Mass)	*0.6 +1 );	-- 60 %
				-- item vel variable
						local b = math.sqrt	(item.Vel.Magnitude	*1.0 +1 );	-- 100 %
				-- part mass variable
						--local c = math.sqrt	(self.Mass +1);

						item.Vel =	item.Vel + forceVector / ( (a + b) / c +1 );

						item.AngularVel = -item.Vel.X/a;

						self.strength = self.strength*0.99;
					end
				end
			end
		end
--[[ lag
		for part in MovableMan.Particles do

			if self.Team < 0 or part.Team ~= self.Team then

				local dist = SceneMan:ShortestDistance(self.Pos,part.Pos,SceneMan.SceneWrapsX);

				if part and dist.Magnitude < self.range then

					strCheck = SceneMan:CastStrengthRay(self.Pos, self.Pos-part.Pos, self.terrPass, Vector(), 2, 0, SceneMan.SceneWrapsX)
					if not(strCheck) then

						local forceVector =	dist:SetMagnitude(
									math.sqrt(self.Vel.Magnitude*self.strength)
									/math.sqrt(dist.Magnitude+1)
									);

				-- part mass variable
						local a = math.sqrt	(math.abs(part.Mass)	*0.7 +1 );	-- 60 %
				-- part vel variable
						local b = math.sqrt	(part.Vel.Magnitude	*1.1 +1 );	-- 100 %
				-- part mass variable
						--local c = math.sqrt	(self.Mass +1);

						part.Vel =	part.Vel + forceVector / ( (a + b) / c +1 );

						self.strength = self.strength*0.999;
					end
				end
			end
		end]]--
	end
end

function Update(self)

	--FrameMan:DrawCirclePrimitive(Vector(self.initPosX,self.initPosY),self.range,254);	-- debug
end
