dofile("Base.rte/Constants.lua")
dofile("Base.rte/Actors/AI/NativeCrabAI.lua")

function Create(self)
	self.AI = NativeCrabAI:Create(self)
	self.soundTimer = Timer();
    self.delay = 180
	self.justSpawned = true;
	self.enableselect = true;
	self.ordersteam = true;
	self.ordersgoto = true;
	self.orderssentry = false;
	self.orderspatrol = true;
end

function Update(self)
	self.justSpawned = false;
	
	if self:IsPlayerControlled() == true then
		if self.enableselect == true then
			self.selected = CreateAEmitter("Tank Select")
			self.selected.Pos = self.Pos
			self.selected.PinStrength = 1000
			MovableMan:AddParticle(self.selected);
			self.enableselect = false
		end
	else
		self.enableselect = true
	end
	
	if self.AIMode == Actor.AIMODE_SQUAD then
		if self.ordersteam == true then
			local sfx = CreateAEmitter("Zss OrderTeam")
			sfx.Pos = self.Pos
			MovableMan:AddParticle(sfx)
			self.ordersteam = false
		end
	else
		self.ordersteam = true
	end
	
	if self.AIMode == Actor.AIMODE_GOTO then
		if self.ordersgoto == true then
			local sfx = CreateAEmitter("Zss OrderActive")
			sfx.Pos = self.Pos
			MovableMan:AddParticle(sfx)
			self.ordersgoto = false
		end
	else
		self.ordersgoto = true
	end
	
	if self.AIMode == Actor.AIMODE_SENTRY then
		if self.orderssentry == true and self.justSpawned == false then
			local sfx = CreateAEmitter("Zss OrderPassive")
			sfx.Pos = self.Pos
			MovableMan:AddParticle(sfx)
			self.orderssentry = false
		end
	else
		self.orderssentry = true
	end
	
	if self.AIMode == Actor.AIMODE_PATROL then
		if self.orderspatrol == true then
			local sfx = CreateAEmitter("Zss OrderPassive")
			sfx.Pos = self.Pos
			MovableMan:AddParticle(sfx)
			self.orderspatrol = false
		end
	else
		self.orderspatrol = true
	end
	
	if self.soundTimer:IsPastSimMS(self.delay) then
		if self:GetController():IsState(Controller.MOVE_LEFT) or self:GetController():IsState(Controller.MOVE_RIGHT) then
			local sfx = CreateAEmitter("Tank Move")
			sfx.Pos = self.Pos
			MovableMan:AddParticle(sfx)
			self.soundTimer:Reset();
		end
	end
	
	if self.Health <= 0 then
 		self:GibThis();
	end
end