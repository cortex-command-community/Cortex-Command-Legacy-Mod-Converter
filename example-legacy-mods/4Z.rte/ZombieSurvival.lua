dofile("Base.rte/Constants.lua")

function ZombieSurvival:StartActivity()

	self.shops = {};
	local box = CreateActor("Mystery Box");
	box.Pos = Vector(SceneMan.SceneWidth / 2, 0);
	box.Pos = SceneMan:MovePointToGround(Vector(math.random(SceneMan.SceneWidth * 0.4, SceneMan.SceneWidth * 0.6), 0), 0, 1) + Vector(0, -ToMOSprite(box):GetSpriteHeight() / 2);
	box.Team = -1;
	MovableMan:AddActor(box);
	table.insert(self.shops, box);

	self.playerTeam = Activity.TEAM_1;
	self.BuyMenuEnabled = false;
	-- some default values
	self.bStr = 1;			-- brain strength multiplier
	self.zStr = 1;			-- enemy strength multiplier

	self.spawnTime = 3000;				-- starting amount of MS between spawns
	self.minSpawnTime = 1000;	-- minimum amount of MS between spawns

	local primaryGroup = "Primary Weapons";
	local secondaryGroup = "Secondary Weapons";
	-- tertiary faction weapon is always a grenade
	local actorGroup = "Light Infantry";

	local defaultActor = ("Ronin Heavy");
	local defaultPrimary = ("Ronin/Spas 12");
	local defaultSecondary = ("Ronin/Peacemaker");
	local defaultTertiary = ("Ronin/Molotov Cocktail");

	if self.Difficulty <= GameActivity.CAKEDIFFICULTY then
		self.bStr = 1.5;	self.zStr = 1.0;

		defaultPrimary = ("Ronin/M60");
		defaultSecondary = ("Ronin/Spas 12");
		defaultTertiary = ("Ronin/Pineapple Grenade");

		primaryGroup = "Heavy Weapons";
		secondaryGroup = "Explosive Weapons";
		actorGroup = "Heavy Infantry";
		self.spawnTime = self.spawnTime - 800;	-- it's easy anyway so spawn zombies faster
	elseif self.Difficulty <= GameActivity.EASYDIFFICULTY then
		self.bStr = 1.5;	self.zStr = 1;

		defaultPrimary = ("Ronin/M16");
		defaultSecondary = ("Ronin/Peacemaker");
		defaultTertiary = ("Ronin/Stick Grenade");

		primaryGroup = "Primary Weapons";
		secondaryGroup = "Light Weapons";
		actorGroup = "Heavy Infantry";
		self.spawnTime = self.spawnTime - 400;
	elseif self.Difficulty <= GameActivity.MEDIUMDIFFICULTY then
		-- medium difficulty = defaults
		actorGroup = "Heavy Infantry";
	elseif self.Difficulty <= GameActivity.HARDDIFFICULTY then
		self.bStr = 1.0;	self.zStr = 1.0;

		defaultActor = ("Ronin Soldier");
		defaultPrimary = ("Ronin/Pumpgun");
		defaultSecondary = ("Ronin/Glock");
		defaultTertiary = ("Ronin/Pineapple Grenade");

		primaryGroup = "Light Weapons";
		secondaryGroup = "Secondary Weapons";
		self.spawnTime = self.spawnTime - 500;
	elseif self.Difficulty <= GameActivity.NUTSDIFFICULTY then
		self.bStr = 0.83;	self.zStr = 1.5;

		defaultActor = ("Ronin Soldier");
		defaultPrimary = ("Ronin/Sawed-off shotgun");
		defaultSecondary = ("Ronin/MAC-10");
		defaultTertiary = ("Ronin/Stick Grenade");

		primaryGroup = "Secondary Weapons";
		secondaryGroup = "Secondary Weapons";
		self.spawnTime = self.spawnTime - 1000;
	elseif self.Difficulty <= GameActivity.MAXDIFFICULTY then
		self.bStr = 0.66;	self.zStr = 1.5;

		defaultActor = ("Ronin Soldier");
		defaultPrimary = ("Ronin/AK-47");
		defaultSecondary = ("Ronin/Peacemaker");
		defaultTertiary = ("Ronin/Molotov Cocktail");

		primaryGroup = "Secondary Weapons";
		secondaryGroup = "Tools";
		self.spawnTime = self.spawnTime - 1500;
	end

	self.startTimer = Timer();
	self.eSpawnTimer = Timer();
	self.survivalTimer = Timer();

	self.lastDeathCountCPU = 0;
	self.killGold = 10;		-- amount of gold for each kill
	self.fogSize = 24;

	MovableMan:OpenAllDoors(true, -1);
	for actor in MovableMan.AddedActors do
		if actor.ClassName == "ADoor" then
			actor.ToSettle = true;
			actor:GibThis();
		end
	end
	ActivityMan:GetActivity():SetTeamFunds(0, self.playerTeam);
	if self:GetFogOfWarEnabled() then
		SceneMan:MakeAllUnseen(Vector(self.fogSize, self.fogSize), self.playerTeam);
	end
	
	self.playerBrains = {};
	
	for player = Activity.PLAYER_1, Activity.MAXPLAYERCOUNT - 1 do
		if self:PlayerActive(player) and self:PlayerHuman(player) then
			local team = self:GetTeamOfPlayer(player);
			local brain = CreateAHuman(defaultActor);
			local tech = PresetMan:GetModuleID(self:GetTeamTech(team));
			if tech ~= -1 then
				-- if a faction was chosen, pick the first item from faction listing
				local module = PresetMan:GetDataModule(tech);
				local primaryWeapon, secondaryWeapon, throwable, actor;
				for entity in module.Presets do
					local picked;	-- prevent duplicates
					if not primaryWeapon and entity.ClassName == "HDFirearm" then
						if ToMOSRotating(entity):HasObjectInGroup(primaryGroup) then
							primaryWeapon = CreateHDFirearm(entity:GetModuleAndPresetName());
							picked = true;
						end
					end
					if not picked and not secondaryWeapon and entity.ClassName == "HDFirearm" then
						if ToMOSRotating(entity):HasObjectInGroup(secondaryGroup) then
							secondaryWeapon = CreateHDFirearm(entity:GetModuleAndPresetName());
							picked = true;
						end
					end
					if not picked and not throwable and entity.ClassName == "TDExplosive" then
						if ToMOSRotating(entity):HasObjectInGroup("Grenades") then
							throwable = CreateTDExplosive(entity:GetModuleAndPresetName());
							picked = true;
						end
					end
					if not picked and not actor and entity.ClassName == "AHuman" then
						if ToMOSRotating(entity):HasObjectInGroup(actorGroup) then
							actor = CreateAHuman(entity:GetModuleAndPresetName());
						end
					end
				end
				if actor then
					brain = actor;
				end
				if primaryWeapon then
					brain:AddInventoryItem(primaryWeapon);
				end
				if secondaryWeapon then
					brain:AddInventoryItem(secondaryWeapon);
				end
				if throwable then
					brain:AddInventoryItem(throwable);
				end
			else
				local weapons = {defaultPrimary, defaultSecondary};
				for i = 1, #weapons do
					local item = CreateHDFirearm(weapons[i]);
					item.GibWoundLimit = 	math.ceil(item.GibWoundLimit * 2 * self.bStr);
					item.JointStrength = 	item.JointStrength * 2 * self.bStr;
					item.GibImpulseLimit = 	item.GibImpulseLimit * 2 * self.bStr;
					brain:AddInventoryItem(item);
				end
				local item = CreateTDExplosive(defaultTertiary);
				if item then
					brain:AddInventoryItem(item);
				end
			end

			local parts = {brain, brain.Head, brain.FGArm, brain.BGArm, brain.FGLeg, brain.BGLeg};
			for i = 1, #parts do
				local limb = parts[i];
				if limb then
					limb.GibWoundLimit = math.ceil(limb.GibWoundLimit * 1.5 * self.bStr);
					limb.DamageMultiplier = limb.DamageMultiplier / self.bStr;
					if IsAttachable(limb) then
						ToAttachable(limb).JointStrength = ToAttachable(limb).JointStrength * 1.5 * self.bStr;
					else	-- body
						limb.GibImpulseLimit = brain.GibImpulseLimit * 1.5 * self.bStr;
					end
				end
			end
-- reinforce FGArm so that we don't lose it
-- no FGArm = no weapons = no gameplay
			brain.FGArm.GibWoundLimit = 999999;
			brain.FGArm.JointStrength = 999999;

			brain.JetTimeTotal = brain.JetTimeTotal * 0.5 * self.bStr;	-- discourage flying

			--local medikit = CreateHDFirearm("Medikit");	-- base.rte
			--if medikit then
			--	brain:AddInventoryItem(medikit);
			--end

			brain.Pos = SceneMan:MovePointToGround(Vector(math.random(0, SceneMan.SceneWidth), 0), 0, 1) + Vector(0, -brain.Diameter);
			brain.Team = team;
			MovableMan:AddActor(brain);
			table.insert(self.playerBrains, brain);
			
			local dots = (20 + brain.Radius) / (self.fogSize * 0.1);
			for i = 0, dots do
				SceneMan:CastSeeRay(brain.Team, brain.Pos, Vector(20 + brain.Diameter, 0):RadRotate(6.28 * i / dots), Vector(), 1, self.fogSize / 2);
			end

			-- Set the found brain to be the selected actor at start
			self:SetPlayerBrain(brain, player);
			self:SwitchToActor(brain, player, team);
			-- Set the observation target to the brain, so that if/when it dies, the view flies to it in observation mode
			self:SetObservationTarget(self:GetPlayerBrain(player).Pos, player);
		end
	end
end

function ZombieSurvival:OnPieMenu()
	--self.PieMenuActor;
	-- remove unnecessary pie slices
	self:RemovePieMenuSlice("Form Squad", "");
	self:RemovePieMenuSlice("Brain Hunt AI Mode", "");
	self:RemovePieMenuSlice("Patrol AI Mode", "");
	self:RemovePieMenuSlice("Gold Dig AI Mode", "");
	self:RemovePieMenuSlice("Go-To AI Mode", "");
	self:RemovePieMenuSlice("Sentry AI Mode", "");
	--
	local closest = 100;
	local foundShop = nil;
	local pieActive = false;
	for i = 1, #self.shops do
		local shop = self.shops[i];
		local dist = SceneMan:ShortestDistance(self.PieMenuActor.Pos, shop.Pos, SceneMan.SceneWrapsX);
		if dist.Magnitude < (self.PieMenuActor.Radius + shop.Radius) and dist.Magnitude < closest then
			closest = dist.Magnitude;
			foundShop = shop;
		end
	end
	if foundShop then
		local funds = self:GetTeamFunds(self.playerTeam);
		local cost = foundShop.Sharpness;
		if funds >= cost and foundShop.Status ~= 1 then
			pieActive = true;
			ZSBuyer = self.PieMenuActor;
			ZSBuyShop = foundShop;
		end
		self:AddPieMenuSlice("Pay Gold", "ZombieSurvivalBuyItem", Slice.UP, pieActive);
	end
end
-- gotta use global values smh
function ZombieSurvivalBuyItem(self)
	if ZSBuyShop and ZSBuyer then
		ZSBuyShop:SetNumberValue("Buyer", ZSBuyer.Team);
		ZSBuyer = nil;
		ZSBuyShop = nil;
	end
end

function ZombieSurvival:EndActivity()
	-- Play sad music if no humans are left
	if self:HumanBrainCount() == 0 then
		AudioMan:ClearMusicQueue();
		AudioMan:PlayMusic("Base.rte/Music/dBSoundworks/udiedfinal.ogg", 2, -1.0);
		AudioMan:QueueSilence(10);
		AudioMan:QueueMusicStream("Base.rte/Music/dBSoundworks/ccambient4.ogg");		
	else
		-- But if humans are left, then play happy music!
		AudioMan:ClearMusicQueue();
		AudioMan:PlayMusic("Base.rte/Music/dBSoundworks/uwinfinal.ogg", 2, -1.0);
		AudioMan:QueueSilence(10);
		AudioMan:QueueMusicStream("Base.rte/Music/dBSoundworks/ccambient4.ogg");
	end
end

function ZombieSurvival:UpdateActivity()

	if self.ActivityState ~= Activity.OVER then
	
		local time = math.floor(self.survivalTimer.ElapsedSimTimeMS / 1000);
		local mins = 1 + math.floor(time / 60);
		local secs = time - (mins - 1) * 60;

		if self:GetTeamDeathCount(self.CPUTeam) > self.lastDeathCountCPU then	-- give 10 gold for every kill
			local deaths = self:GetTeamDeathCount(self.CPUTeam) - self.lastDeathCountCPU;
			self:SetTeamFunds(self:GetTeamFunds(self.playerTeam) + self.killGold * deaths, self.playerTeam);
		end
		--[[
		for i = 1, #self.playerBrains do
			local brain = self.playerBrains[i];
			if brain and IsActor(brain) then
		]]--
		local brainCount = 0;
		local players = {};
		for player = Activity.PLAYER_1, Activity.MAXPLAYERCOUNT - 1 do
			if self:PlayerActive(player) and self:PlayerHuman(player) then
				table.insert(players, player);

				local brain = self:GetPlayerBrain(player);

				if self.startTimer:IsPastSimMS(3000) then
					FrameMan:SetScreenText(mins - 1 .. " minutes " .. secs .. " seconds | " .. self:GetTeamDeathCount(self.CPUTeam) .. " kills", player, 0, 1000, false);
				else
					FrameMan:SetScreenText("Survive for as long as possible!", player, 333, 5000, true);
				end
				-- The current player's team
				local team = self:GetTeamOfPlayer(player);
				-- Check if player's brain is alive
				if brain and MovableMan:IsActor(brain) then
					local ctrl = brain:GetController();
					
					brainCount = brainCount + 1;
					
					if brain.Vel.Magnitude < 15 and
					not ctrl:IsState(Controller.BODY_JUMP) and
					not ctrl:IsState(Controller.BODY_JUMPSTART) and
					not ctrl:IsState(Controller.BODY_CROUCH) then

						local brainVel = math.ceil(brain.Vel.Magnitude + 0.1);	-- to avoid division by zero
						local xCheck = 2 * brain.Radius * brainVel;

						local groundCheck = SceneMan:CastStrengthRay(brain.Pos, Vector(0, brain.Height / 4), 10, Vector(), 0, 0, SceneMan.SceneWrapsX);
						local wallCheck = SceneMan:CastStrengthRay(brain.Pos, Vector(xCheck, 0), 10, Vector(), 0, 0, SceneMan.SceneWrapsX);
						if groundCheck and not(wallCheck) then

							if ctrl:IsState(Controller.MOVE_RIGHT) then
								brain.Vel = brain.Vel + Vector(self.bStr / brainVel, 0);	-- speed also affected by difficulty
							end
							if ctrl:IsState(Controller.MOVE_LEFT) then
								brain.Vel = brain.Vel + Vector(-self.bStr / brainVel, 0);
							end
						end
					end
					self:SetActorSelectCursor(brain.Pos, player);	-- prevent looking around
				else
					-- Get any AHuman actor that the player could use
					for actor in MovableMan.Actors do
						if IsAHuman(actor) and actor.Health > 0 and actor.Team == self.playerTeam then
							foundBrain = actor;
							break;
						end
					end
					if foundBrain then
						self:SetPlayerBrain(foundBrain, player);
						self:SwitchToActor(foundBrain, player, self:GetTeamOfPlayer(player));
						self:SetObservationTarget(self:GetPlayerBrain(player).Pos, player);
						brainCount = brainCount + 1;
						self:GetBanner(GUIBanner.RED, player):ClearText();
					else
						self:SetPlayerBrain(nil, player);
						FrameMan:ClearScreenText(player);
						FrameMan:SetScreenText("Oh no, you're dead!", player, 333, -1, false);
					end
				end
			end
		end
		if brainCount == 0 then
			for i = 1, #players do
				local player = players[i];
				self:ResetMessageTimer(player);
				FrameMan:ClearScreenText(player);
				FrameMan:SetScreenText("You survived for " .. mins - 1 .. " minutes " .. secs .. " seconds! Kills: " .. self:GetTeamDeathCount(self.CPUTeam), player, 333, -1, false);
			end
			self.WinnerTeam = self:OtherTeam(self.playerTeam);
			ActivityMan:EndActivity();
		end
		-- handle enemy spawning
		local cpuCount = math.ceil(MovableMan:GetTeamMOIDCount(self.CPUTeam) / 6);	-- each zombie is an average of 6 MOIDs
		if self.eSpawnTimer:IsPastSimMS(self.spawnTime + (cpuCount * self.spawnTime * 0.1)) and self.CPUTeam ~= Activity.NOTEAM then
			self.eSpawnTimer:Reset();
			-- check player brains
			local brains = {};
			local needHealing = false;
			for player = Activity.PLAYER_1, Activity.MAXPLAYERCOUNT - 1 do
				if self:PlayerActive(player) and self:PlayerHuman(player) then
					local foundBrain = self:GetPlayerBrain(player);
					if foundBrain then
						table.insert(brains, foundBrain);
						if foundBrain.Health < (foundBrain.MaxHealth / 2) then
							needHealing = true;
						end
					end
				end
			end
			-- check for enemies that might be stuck before spawning more
			local teleport = false;
			for actor in MovableMan.Actors do
				if actor.Age > (self.spawnTime * 10) and actor.Status < 3 and actor.Team == self.CPUTeam then
					local valid = true;
					local dist = Vector(0, 0);
					local width = FrameMan.ResX * 0.8;
					for i = 1, #brains do
						dist = SceneMan:ShortestDistance(Vector(actor.Pos.X, 0), Vector(brains[i].ViewPoint.X, 0), SceneMan.SceneWrapsX);
						if dist.Magnitude < width then	-- don't teleport if too close to a player
							valid = false;
						else
							dist:SetMagnitude(math.abs(dist.X) - width);
						end
					end
					if valid then
						actor.Pos = SceneMan:MovePointToGround(Vector(actor.Pos.X + dist.X, 0), 0, 1);
						--print("Zombie number ".. actor.ID .." jumped ".. math.floor(dist.X + 0.5) .." pixels!");
						--actor:FlashWhite(10000);
						teleport = true;
						break;
					end
				end
			end
			if (not teleport or math.random(100) < self.Difficulty) and cpuCount < (rte.AIMOIDMax / 4) then
				-- spawn new enemy
				local enemy = CreateAHuman("4Z/4Zombie");
				if self.spawnTime < (self.minSpawnTime * 3.6) then
					local rand = math.random();
					if rand < 0.2 then
						enemy = CreateAHuman("4Z/4Zombie Spitter");
					elseif rand < 0.4 and self.spawnTime < (self.minSpawnTime * 3.3) then
						enemy = CreateAHuman("4Z/4Zombie Bloater");
					elseif rand < 0.43 and self.spawnTime < (self.minSpawnTime * 3.0) then
						enemy = CreateAHuman("4Z/Ankou");
					end
					--if needHealing and math.random() < 0.05 then
					--	local medikit = CreateHDFirearm("Medikit");
					--	if medikit then
					--		enemy:AddInventoryItem(medikit);
					--	end
					--end
				end
				enemy.Team = self.CPUTeam;
				-- buff enemy based on difficulty
				local parts = {enemy, enemy.Head, enemy.FGArm, enemy.BGArm, enemy.FGLeg, enemy.BGLeg};
				for i = 1, #parts do
					parts[i].GibWoundLimit = math.ceil(parts[i].GibWoundLimit * self.zStr);
					parts[i].DamageMultiplier = parts[i].DamageMultiplier / self.zStr;
					if IsAttachable(parts[i]) then
						parts[i].JointStrength = parts[i].JointStrength * self.zStr;
					else
						parts[i].GibImpulseLimit = parts[i].GibImpulseLimit * self.zStr;
					end
				end
				enemy:SetLimbPathSpeed(1, enemy:GetLimbPathSpeed(1) * self.zStr);
				-- calculate spawn point
				if SceneMan.SceneWrapsX then
					if SceneMan.SceneWidth > FrameMan.ResX then
						-- figure out how to spawn enemy the furthest possible off screen: "pillar" method
						local x = 0;
						local dist = Vector(0, 0);
						local points = {};
						local dots = #brains + 3;
						local chunk = SceneMan.SceneWidth / dots;
						local width = FrameMan.ResX * 0.6;
						for a = 1, dots do
							local pillar = chunk * a;
							local valid = true;
							for b = 1, #brains do
								dist = SceneMan:ShortestDistance(Vector(brains[b].ViewPoint.X, 0), Vector(pillar, 0), SceneMan.SceneWrapsX);
								if dist.Magnitude < width then
									valid = false;	-- process of elimination
								else
									dist:SetMagnitude(math.abs(dist.X) - width);
								end
							end
							if valid then
								table.insert(points, {pillar, dist.X});
							end
						end
						local pillar = math.random(#points);
						x = points[pillar][1];
						enemy.Pos = SceneMan:MovePointToGround(Vector(x + math.random(-points[pillar][2], points[pillar][2]), 0), 0, 1);
					else
						enemy.Pos = SceneMan:MovePointToGround(Vector(math.random(SceneMan.SceneWidth), 0), 0, 1);
					end
				else	-- spawning at edge
					local edge = 1;
					local x = 1;
					if math.random() < 0.5 then
						edge = SceneMan.SceneWidth -1;
						x = -1;
						enemy.HFlipped = true;
					end
					enemy.Pos = SceneMan:MovePointToGround(Vector(edge, 0), 0, 1) - Vector(x * 20, 0);
					enemy.Vel = Vector(x * 5, -5) * RangeRand(1.0, 2.0);	-- "jump" out
				end
				MovableMan:AddActor(enemy);
				-- set AI mode
				enemy.AIMode = Actor.AIMODE_BRAINHUNT;	-- default to this if no assigned brains found
				if #brains > 0 then
					enemy.AIMode = Actor.AIMODE_GOTO;
					enemy:AddAIMOWaypoint(brains[math.random(#brains)]);	-- pick one of the found player brains as the target
				end
			end
		end
		if self.spawnTime > self.minSpawnTime then
			self.spawnTime = self.spawnTime * 0.99999;	-- spawn time gets gradually denser
		elseif not self.maxSpawnTimeReached then
			self.maxSpawnTimeReached = true;
			print("maximum spawn time reached!");
		end
	end
	self.lastDeathCountCPU = self:GetTeamDeathCount(self.CPUTeam);
end