-- thanks to filipex and pawnis

function Create(self)

	self:SetNumberValue("Randomization", math.random(0, 4))
	
	if self.HFlipped then
		self.DefaultStanceOffset = Vector(-self.StanceOffset.X,self.StanceOffset.Y)
	else
		self.DefaultStanceOffset = self.StanceOffset
	end
	
	
	self.stab_timer = Timer();
	self.stab_angle = 0
	self.stab_lasts = false
	self.stab_dmg = true
	self.equipped_by_actor = false
	
	--self.can_activate_timer = Timer()
	--self.activate_time = 60000/self.RateOfFire
	
	local actor = MovableMan:GetMOFromID(self.RootID);
	if actor and IsAHuman(actor) then
		self.parent = ToAHuman(actor);
	end
end

function Update(self)

	--check if flipped
	local mir
	if self.HFlipped then
		mir = -1;
	else
		mir = 1;
	end
	
	--check user
	local actor = MovableMan:GetMOFromID(self.RootID);
	if actor and IsAHuman(actor) then
		self.parent = ToAHuman(actor);
		self.parent:GetController():SetState(Controller.AIM_SHARP, false);
		self.equipped_by_actor = true;
	else
		self.parent = nil;
		self.equipped_by_actor = false;
	end
	
	if self.disableFire == true and self.equipped_by_actor == true then
		self.parent:GetController():SetState(Controller.WEAPON_FIRE,false);		
	end
	
	if self.parent then
			
		if self:IsActivated() or (self.stab_timer:IsPastSimMS(400) and self.stab_lasts == true) then
		
			if self.parent then
				self.disableFire = true;
			end
			
			if self.stab_angle >= 1.57 then
				self:Deactivate();
			else
				self:Activate();
			end
			
			self.StanceOffset = Vector(self.DefaultStanceOffset.X*2,self.DefaultStanceOffset.Y*0.5)
			if self.stab_timer:IsPastSimMS(200) and self.stab_lasts == true then
				self.stab_lasts = false
			end
			
			if self:IsActivated() then self.stab_lasts = true end
			self.parent:GetController():SetState(Controller.AIM_SHARP, false)
			self.stab_angle = (self.stab_angle + math.pi*0.5)/2
			if self.stab_timer:IsPastSimMS(100) then
				
				if self.stab_dmg then
					local Vector2 = (Vector(2,0):GetXFlipped(self.HFlipped)):RadRotate(self.RotAngle)

					self.ray = SceneMan:CastMORay(self.Pos+Vector(0, -4), Vector2, self.RootID, self.Team, 128, false, 2);

					if self.ray > 0 then								
						for i = 1, 1 do
							local Effect = CreateMOPixel("Particle Knife", "ScrapperFaction.rte")
							if Effect then
								Effect.Vel = self.Vel + (Vector(65, 0):GetXFlipped(self.HFlipped):RadRotate(self.RotAngle));
								Effect.Pos = self.Pos + (Vector(0, -1):RadRotate(self.RotAngle));
								Effect.Team = self.Team;
								Effect.IgnoresTeamHits = true;
								MovableMan:AddParticle(Effect);							
							end
						end
					end
					self.stab_dmg = false
				end
			end
		else
			self.StanceOffset = self.DefaultStanceOffset
			self.stab_dmg = true
			if self.stab_angle > 0.001 then
				self.stab_angle = self.stab_angle*0.5
			else
				self.disableFire = false;
			end
		end
		
		self.RotAngle = self.RotAngle-(self.stab_angle*mir)
		self:SetNumberValue("RotAngle", self.RotAngle)
		self:SetNumberValue("AngularVel", self.AngularVel)
	else
		self:SetNumberValue("RotAngle", self.RotAngle)
		self:SetNumberValue("AngularVel", self.AngularVel)
	end
	
end