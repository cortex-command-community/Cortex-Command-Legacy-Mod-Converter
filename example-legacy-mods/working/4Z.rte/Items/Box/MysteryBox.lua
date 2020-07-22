function Create(self)
	self.teddyChance = 0.01;	-- Chance of box getting destroyed
	self.teddyFactor = 1.4;		-- How much the chance increases on each spin
	
	self.spinCost = 100;
	self.itemTable = {};
	local totalCost = 0;
	for module in PresetMan.Modules do
		for entity in module.Presets do
			if (entity.ClassName == "HDFirearm" or entity.ClassName == "TDExplosive" or entity.ClassName == "HeldDevice") and not ToMOSRotating(entity):HasObjectInGroup("Bombs - Payloads") and ToMOSRotating(entity).IsBuyable then
				table.insert(self.itemTable, entity);
				totalCost = totalCost + ToMOSRotating(entity):GetGoldValue(0, 1, 1);
			end
		end
	end
	self.spinCost = math.ceil(totalCost / #self.itemTable / 10) * 10;
	print("Added a total of ".. #self.itemTable .." items into the Mystery Box!");
	print("The cost of the Mystery Box is now ".. self.spinCost);
	self.Sharpness = self.spinCost;
	
	self.updateTimer = Timer();
	self.updateTime = 50;
	
	self.rand = 0;
	self.randFactor = 1.2;
end
function Update(self)
	self.Health = self.MaxHealth;
	self.Frame = 0;
	-- Unpin picked up items
	if self.drop then
		self.Frame = 1;
		if self.drop.ID ~= self.drop.RootID or self.drop.PinStrength ~= 1 then
			self.drop.PinStrength = 0;
			self.drop = nil;
		else
			FrameMan:DrawBitmapPrimitive(self.drop.Pos, self.drop, 0, 0);
		end
	end
	if self.spawnTimer then
		self.Frame = 1;
		self.Status = 1;
		if self.updateTimer:IsPastSimMS(self.updateTime) then
			self.updateTimer:Reset();
			self.updateTime = self.updateTime * self.randFactor;
			self.rand = math.random(#self.itemTable);
			if math.random() < self.teddyChance then
				self.rand = 0;
			end
			AudioMan:PlaySound("Base.rte/Sounds/Geiger".. math.random(3) ..".wav ", SceneMan:TargetDistanceScalar(self.Pos) / 2, false, true, -1);
		end
		local item = CreateTDExplosive("Deathmatch.rte/Teddy");	-- 0
		if self.rand ~= 0 then
			local entity = self.itemTable[self.rand];
			if entity.ClassName == "HDFirearm" then
				item = CreateHDFirearm(entity:GetModuleAndPresetName());
			elseif entity.ClassName == "TDExplosive" then
				item = CreateTDExplosive(entity:GetModuleAndPresetName());
			elseif entity.ClassName == "HeldDevice" then
				item = CreateHeldDevice(entity:GetModuleAndPresetName());
			end
		end
		item.Pos = self.spawnPos;
		if self.spawnTimer:IsPastSimMS(self.spawnDelay) then
			local sound = "SlicePicked2.wav";
			item.Pos = self.spawnPos;
			item.PinStrength = 1;
			MovableMan:AddItem(item);
			self.drop = item;
			self.spawnTimer = nil;
			if self.rand == 0 then
				sound = "Error.wav";
				item:Activate();
				self.RotAngle = 0;
				local x = 0;
				if SceneMan.SceneWrapsX then
					x = self.Pos.X + math.random(SceneMan.SceneWidth * 0.3, SceneMan.SceneWidth * 0.7);
				else
					x = math.random(SceneMan.SceneWidth * 0.2, SceneMan.SceneWidth * 0.8);
				end
				self.Pos = SceneMan:MovePointToGround(Vector(x, 0), 0, 1) + Vector(0, -ToMOSprite(self):GetSpriteHeight() / 2);
				self.teddyChance = 0.01;
				--self.MissionCritical = false;
				--self:GibThis();
			else
				item:Deactivate();
				self.teddyChance = self.teddyChance * self.teddyFactor;
			end
			AudioMan:PlaySound("Base.rte/GUIs/Sounds/".. sound, SceneMan:TargetDistanceScalar(self.Pos) / 2, false, true, -1);
		else
			self.spawnPos.Y = self.spawnPos.Y - (5 / (1 + self.spawnTimer.ElapsedSimTimeMS * 0.1));
			FrameMan:DrawBitmapPrimitive(self.spawnPos, item, 0, 0);
			local size = {10, 20, 30, 40, 50};
			local glowSize = size[1];
			for i = 1, #size do
				if item.Diameter < size[i] then
					glowSize = size[i];
					break;
				end
			end
			local glow = CreateMOPixel("Mystery Box Glow ".. glowSize);
			glow.Pos = Vector(self.spawnPos.X, self.spawnPos.Y);
			MovableMan:AddParticle(glow);
		end
	else
		self.Status = 0;
		self.updateTime = 50;
		self.rand = math.random(#self.itemTable);
		if self:NumberValueExists("Buyer") then
			self.spawnTimer = Timer();
			self.spawnPos = Vector(self.Pos.X, self.Pos.Y);
			ActivityMan:GetActivity():SetTeamFunds(ActivityMan:GetActivity():GetTeamFunds(self:GetNumberValue("Buyer")) - self.spinCost, self:GetNumberValue("Buyer"));
			self.randFactor = RangeRand(1.05, 1.1);
			self.spawnDelay = math.random(4000, 5000);
			if self.drop then
				self.drop.ToDelete = true;
				self.drop = nil;
			end
			self:RemoveNumberValue("Buyer");
			AudioMan:PlaySound("Base.rte/GUIs/Sounds/PieMenuEnter1.wav", SceneMan:TargetDistanceScalar(self.Pos) / 2, false, true, -1);
		end
	end
end