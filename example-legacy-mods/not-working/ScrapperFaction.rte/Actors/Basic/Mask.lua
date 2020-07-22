function Create(self)
    local framesForTeams = {}; --Setup a table to hold the frames for each team
    local maxFrame = 6; --Figure out how many frames each team gets, this must be the same for each team right now
    
    --Go through each team in the activity so we can add the correct frames for them
    for team = 0, ActivityMan:GetActivity().TeamCount - 1 do
        framesForTeams[team] = {}; --Setup a table subtable for the team, this is just a necessary part of Lua
        
        --Count from 0 to the max number of frames
        for i = 0, maxFrame do
            --Add an entry to the table we made for the team, the calculation works by the following logic:
            --multiply the max frame by the team to get how much we add to our current count we're at, because the first team is 0, this will add 0 for that team and 6 to the next team and so on
            table.insert(framesForTeams[team], i + maxFrame*team);
        end
    end
    self.Frame = framesForTeams[self.Team][math.random(#framesForTeams[self.Team])]; --Set the frame to be a random one in the table for our team
    
    --IF YOU WANT TO SEE ALL THE ENTRIES IN THE TABLE, UNCOMMENT THIS CODE:
    for team, table in pairs(framesForTeams) do
        print("Entry for team "..tostring(team)..": "..table.concat(table, ", "));
    end
end