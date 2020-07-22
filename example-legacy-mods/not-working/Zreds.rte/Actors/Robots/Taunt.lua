function Taunt(self)
	local sfx = CreateAEmitter("Taunt Zss")
	sfx.Pos = self.Pos
	MovableMan:AddParticle(sfx)
end