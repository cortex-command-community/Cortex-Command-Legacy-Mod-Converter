function Create(self)
	self.effectRangeX = FrameMan.ResX * 0.4;	-- Reaches every actor on screen
	self.effectRangeY = 50;	-- Affects actors on approximately same height level
	self.shake = 50;	-- Camera shake intensity
	
	self.lifeTimer = Timer();
	self.shakeTimer = Timer();
end
function Update(self)
	self.AngularVel = self.AngularVel * 0.9;
	self.RotAngle = self.RotAngle * 0.9;
	self.Frame = 0;
	self.ToSettle = false;
	if self.shakeTable then	-- Activated, dispense earthquake effect!
		self.Frame = 1;
		if self.shakeTimer:IsPastSimMS(self.shake) then
			self.shakeTimer:Reset();
			for i = 1, #self.shakeTable do
				local actor = self.shakeTable[i];
				if actor and IsActor(actor) then
					ToActor(actor).ViewPoint = ToActor(actor).ViewPoint + Vector(0, self.shake);
				end
			end
		end
		if self.lifeTimer:IsPastSimMS(500) then
			self.ToDelete = true;
		end
	elseif self.Vel.Magnitude > 5 then
		local terrCheck = 0;
		local pos = {Vector(9, 0), Vector(0, 9), Vector(-9, 0), Vector(0, -9), Vector(8, 8), Vector(-8, 8), Vector(-8, -8), Vector(8, -8)};
		for i = 1, #pos do
			local checkPos = self.Pos + Vector(self.Vel.X, self.Vel.Y) * 0.3 + pos[i];
			local terrCheck = SceneMan:GetTerrMatter(checkPos.X, checkPos.Y);
			if terrCheck ~= 0 then
				-- Wreck shit
				self.shakeTable = {};
				self.Mass = self.Mass / 4;
				self.lifeTimer:Reset();
				for actor in MovableMan.Actors do
					local dist = SceneMan:ShortestDistance(self.Pos, actor.Pos, SceneMan.SceneWrapsX);
					local length = 1;
					if actor.Status < 1 then
						if IsAHuman(actor) then
							actor = ToAHuman(actor);
							if actor.FGLeg then
								length = ToMOSprite(actor.FGLeg):GetSpriteWidth() * (actor.FGLeg.Frame / actor.FGLeg.FrameCount);
							elseif actor.BGLeg then
								length = ToMOSprite(actor.BGLeg):GetSpriteWidth() * (actor.BGLeg.Frame / actor.BGLeg.FrameCount);
							end
						elseif IsACrab(actor) then
							actor = ToACrab(actor);
							if actor.RFGLeg then
								length = actor.RFGLeg.Radius;
							elseif actor.LFGLeg then
								length = actor.LFGLeg.Radius;
							end
						end
					end
					if dist.Magnitude < self.effectRangeX then
						table.insert(self.shakeTable, actor);
						if math.abs(actor.Vel.Y) < 5 and math.abs(actor.Pos.Y - self.Pos.Y) < self.effectRangeY and actor.MissionCritical ~= true then
							length = length + 1 + ToMOSprite(actor):GetSpriteHeight() / 2;
							local hitPos = Vector(0, 0);
							local terrCheck = SceneMan:CastStrengthRay(actor.Pos, Vector(0, length), 1, hitPos, math.sqrt(length), 0, SceneMan.SceneWrapsX);
							if terrCheck then
								actor.Health = 0;
								actor.Vel = actor.Vel / 2 - Vector(0, 10);
								actor.AngularVel = actor.AngularVel / 2 + math.random(-10, 10);
								hitPos = hitPos + Vector(0, -length / 2);
								local particleCount = 4;
								for i = 1, particleCount do
									local part = CreateMOSParticle("Mario.rte/Hit Effect Tiny Star");
									part.Lifetime = part.Lifetime * RangeRand(0.5, 1.0);
									part.Pos = hitPos;
									part.Vel = Vector((5 + math.sqrt(actor.Radius)), 0):RadRotate(0.79 + 6.28 * (i / particleCount)) + Vector(0, -5);
									MovableMan:AddParticle(part);
								end
								local glow = CreateMOPixel("Mario.rte/Hit Effect Star Glow");
								glow.Pos = hitPos;
								MovableMan:AddParticle(glow);
								AudioMan:PlaySound("Mario.rte/Sounds/smw/smw_stomp.wav", SceneMan:TargetDistanceScalar(actor.Pos) / 3, false, true, -1);
							end
						end
					end
				end
				local glow = CreateMOPixel("Mario.rte/Hit Effect Star Glow");
				glow.Pos = checkPos;
				MovableMan:AddParticle(glow);
				local particleCount = 200;
				for i = 1, particleCount do
					local part = CreateMOPixel("Mario.rte/Terrain Damager");
					local outVec = Vector(4, 0):RadRotate(6.28 * (i / particleCount));
					part.Vel = Vector(outVec.X * self.effectRangeX * 0.1, outVec.Y * self.effectRangeY * 0.1);
					part.Pos = self.Pos + Vector(0, 4) + part.Vel * 0.1;
					part.Mass = part.Mass / (1 + part.Vel.Magnitude);
					MovableMan:AddParticle(part);
				end 
				local sfx = CreateAEmitter("Mario.rte/POW Thud");	-- High priority
				sfx.Pos = self.Pos;
				MovableMan:AddParticle(sfx);
				break;
			end
		end
	elseif self.Vel.Magnitude < 2 and self.lifeTimer:IsPastSimMS(500) then
		self.ToSettle = true;
	else
		self.lifeTimer:Reset();
	end
	self.HFlipped = false;
end