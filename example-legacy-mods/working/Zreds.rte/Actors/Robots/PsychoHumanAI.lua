-- originally created by clunatic
dofile("Base.rte/Constants.lua")
dofile("Zreds.rte/Actors/Robots/MeleeNativeHumanAI.lua")		--Change this to point to the right location

function Create(self)
	self.AI = MeleeNativeHumanAI:Create(self)
	self.soundTimer = Timer();
    self.delay = 2000    -- cooldown before another sound can play, in MS
    self.dmgLimit = 2    -- how much damage has to be dealt at once for sound to play
    self.lastHealth = self.Health
	self.justSpawned = true;
	self.enableselect = true;
	self.ordersteam = true;
	self.ordersgoto = true;
	self.orderssentry = false;
	self.orderspatrol = true;
	self.ordersdig = true;
	self.ordershunt = true;
end

function Update(self)
	self.justSpawned = false;
	
	if self.soundTimer:IsPastSimMS(self.delay) then
		if self.Health < self.lastHealth-self.dmgLimit and self:IsDead() == false then
			local sfx = CreateAEmitter("Pain Zss")
			sfx.Pos = self.Pos
			MovableMan:AddParticle(sfx)
			self.soundTimer:Reset();
		end
	end
	self.lastHealth = self.Health
	
	if self:IsPlayerControlled() == true then
		if self.enableselect == true then
			self.selected = CreateAEmitter("Psycho Select")
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
	
	if self.AIMode == Actor.AIMODE_GOLDDIG then
		if self.ordersdig == true then
			local sfx = CreateAEmitter("Zss OrderPassive")
			sfx.Pos = self.Pos
			MovableMan:AddParticle(sfx)
			self.ordersdig = false
		end
	else
		self.ordersdig = true
	end
	
	if self.AIMode == Actor.AIMODE_BRAINHUNT then
		if self.ordershunt == true then
			local sfx = CreateAEmitter("Zss OrderAttack")
			sfx.Pos = self.Pos
			MovableMan:AddParticle(sfx)
			self.ordershunt = false
		end
	else
		self.ordershunt = true
	end
end

function UpdateAI(self)
	self.AI:Update(self)
end