SLASH_HELLOWORLD1, SLASH_HELLOWORLD2 = '/hiw', '/hellow'; -- 3.
function SlashCmdList.HELLOWORLD(msg, editbox) -- 4.
	print("Hello, World!");
end
SLASH_BLAH1 = "/blah"
SlashCmdList["BLAH"] = function(msg, editBox)
    -- change the text on the editBox.
    editBox:Show()
    editBox:SetText("Blah blah blah!")
end	

function MyAddon_Mimic(who, send)
	local posX, posY = GetPlayerMapPosition(who);
	if send==1 then
		DEFAULT_CHAT_FRAME:AddMessage(who .. " is currently at location " .. posX .. "," .. posY)
	end
end

function MyAddon_Call()
	MyAddon_Mimic("AucTest", 1)
	MyAddon_Mimic("party1", 1)
	MyAddon_Mimic("party2", 0)
end

--MyAddon_Call()
local frame = CreateFrame("FRAME", "FooAddonFrame");
--frame:RegisterEvent("PLAYER_ENTERING_WORLD");

frame:RegisterEvent("AUCTION_HOUSE_SHOW");
local function eventHandler(self, event, ...)
	print("Hello World! Hello " .. event);
	if event == "AUCTION_HOUSE_SHOW" then
		frame:RegisterEvent("AUCTION_ITEM_LIST_UPDATE")
		_,flag = CanSendAuctionQuery()
		if flag then
			QueryAuctionItems("", "", "", nil, nil, nil, 0, nil, nil, true);
		else
			print("cannot query getall")
		end
	end
	if event == "AUCTION_ITEM_LIST_UPDATE" then
		local batch,num = GetNumAuctionItems("list")
		print(batch,num)
		AucScanData = {}
		AucChance = {}
		for i=1,batch do
			itemData = {}
			print(i)
			local name, _, count, quality, canUse, level, _, minBid, minIncrement, buyoutPrice, bidAmount, highBidder, bidderFullName, owner, ownerFullName, saleStatus, itemId = GetAuctionItemInfo("list", i)
			local itemLink = GetAuctionItemLink("list", i)
			local _, _, _, _, _, _, _, _, _, _, itemSellPrice = GetItemInfo(itemLink)
			itemData["itemId"] = itemId
			itemData["name"] = name
			itemData["count"] = count
			itemData["quality"] = quality
			itemData["canUse"] = canUse
			itemData["level"] = level
			itemData["minBid"] = minBid
			itemData["minIncrement"] = minIncrement
			itemData["buyoutPrice"] = buyoutPrice
			itemData["bidAmount"] = bidAmount
			itemData["highBidder"] = highBidder
			itemData["bidderFullName"] = bidderFullName
			itemData["owner"] = owner
			itemData["ownerFullName"] = ownerFullName
			itemData["saleStatus"] = saleStatus
			itemData["vendorPrice"] = itemSellPrice
			--if count >= 1 then
			local highBid
			if bidAmount > 0 then
				highBid = bidAmount
			else
				highBid = minBid
			end
			print("itemId",itemId)
			print("highBid",highBid)
			local bidPer = highBid / count
			local buyoutPer = buyoutPrice / count
			print(bidPer,buyoutPer,count)
			if itemId == 82800 then
				itemSellPrice = 10000
			end
			if bidPer < itemSellPrice then
				vendorInfo = itemId..' '..bidPer..' '..buyoutPer..' '..itemSellPrice
				AucChance[itemId] = AucChance[itemId]..'\n'..vendorInfo
			end
			AucScanData[i] = itemData		
		end
		print("everything is done")
		frame:UnregisterEvent("AUCTION_ITEM_LIST_UPDATE")
		--PlayerName = UnitName("player");
		--PlayerRealm = GetRealmName();
		--PlayerFaction = UnitFactionGroup("player");
		--print(PlayerName,PlayerRealm,PlayerFaction);
	end
end
frame:SetScript("OnEvent", eventHandler);