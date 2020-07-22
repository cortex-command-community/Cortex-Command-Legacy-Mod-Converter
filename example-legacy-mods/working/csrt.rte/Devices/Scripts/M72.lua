function Create(self)
end

function Update(self)
	if ToMagazine(self.Magazine).RoundCount == 0 then
		self:GibThis()
	end
end