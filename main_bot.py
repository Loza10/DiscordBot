import discord
from discord.ext import commands, tasks
import os
import pandas as pd
import math
import csv
from sklearn.linear_model import LinearRegression
import datetime
from datetime import date
from openai import OpenAI

client = OpenAI(
    api_key="INSERT HERE!!",
)

placementData = pd.read_csv("global_data/place.csv", sep=',', header=0).to_numpy()
challengeData = pd.read_csv("global_data/chal.csv", sep=',', header=0).to_numpy()
tribalattendedData = pd.read_csv("global_data/tribal.csv", sep=',', header=0).to_numpy()
votesrecievedData = pd.read_csv("global_data/vote.csv", sep=',', header=0).to_numpy()

placementData_tuples = [(row[0], row[-1]) for row in placementData]

playerList = (pd.read_csv("global_data/place.csv", sep=',', header=0)['Players'].to_numpy())

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

seasons = [{"Number": "1", "Theme": "The Jungle", "Castsize": "16", "Host(s)": "Ryfri", "Date": "30 Dec. 2017", "Winner": "Spongey"},
           {"Number": "2", "Theme": "Four Seas", "Castsize": "16", "Host(s)": "Keegle & Spongey", "Date": "13 Jan. 2018", "Winner": "MajorWoof"},
           {"Number": "3", "Theme": "Cold Shoulder", "Castsize": "18", "Host(s)": "Austin & Keegle", "Date": "17 Feb. 2018", "Winner": "Jared"},
           {"Number": "4", "Theme": "Desert Oasis", "Castsize": "21", "Host(s)": "Spongey", "Date": "10 Mar. 2018", "Winner": "dontbow"},
           {"Number": "5", "Theme": "Exile Island", "Castsize": "18", "Host(s)": "CHANGA & Dahii", "Date": "7 Apr. 2018", "Winner": "Merc"},
           {"Number": "6", "Theme": "HvV", "Castsize": "18", "Host(s)": "Ryfri & Phoraxe", "Date": "2 Jun. 2018", "Winner": "Spongey"},
           {"Number": "7", "Theme": "The Tropics", "Castsize": "21", "Host(s)": "Keegle & Swishduck", "Date": "30 Jun. 2018", "Winner": "Peridot"},
           {"Number": "8", "Theme": "Inferior", "Castsize": "15", "Host(s)": "Jared", "Date": "10 Aug. 2018", "Winner": "Zevulpes"},
           {"Number": "9", "Theme": "Seasons Change", "Castsize": "20", "Host(s)": "Spongey & Dahii", "Date": "15 Sep. 2018", "Winner": "Bjr"},
           {"Number": "10", "Theme": "Space Legacy", "Castsize": "18", "Host(s)": "Keegle & Ryfri", "Date": "10 Nov. 2018", "Winner": "Lucity"},
           {"Number": "11", "Theme": "Winter is Coming", "Castsize": "20", "Host(s)": "Theb & CHANGA", "Date": "27 Dec. 2018", "Winner": "KOKE"},
           {"Number": "12", "Theme": "David vs Goliath", "Castsize": "20", "Host(s)": "Zevulpes & Lucity", "Date": "26 Jan. 2019", "Winner": "Andy"},
           {"Number": "13", "Theme": "Avatar", "Castsize": "20", "Host(s)": "Keegle & Spongey", "Date": "9 Mar. 2019", "Winner": "Purpdan"},
           {"Number": "14", "Theme": "Apocalypse", "Castsize": "19", "Host(s)": "Garrett & Keegle", "Date": "27 Apr. 2019", "Winner": "Tuxpeng"},
           {"Number": "15", "Theme": "Olympians", "Castsize": "20", "Host(s)": "Spongey & Andy", "Date": "1 Jun. 2019", "Winner": "Keegle"},
           {"Number": "16", "Theme": "Reunion", "Castsize": "18", "Host(s)": "Swishduck & Keegle", "Date": "14 Jul. 2019", "Winner": "zCent"},
           {"Number": "17", "Theme": "Rodeo", "Castsize": "21", "Host(s)": "Peridot & Pie", "Date": "24 Aug. 2019", "Winner": "Spongey"},
           {"Number": "18", "Theme": "Atlantis", "Castsize": "18", "Host(s)": "zCent", "Date": "21 Sep. 2019", "Winner": "Bizzlebub"},
           {"Number": "19", "Theme": "The Mines", "Castsize": "16", "Host(s)": "Keegle", "Date": "9 Nov. 2019", "Winner": "PotaTomas"},
           {"Number": "20", "Theme": "Ghost Island", "Castsize": "21", "Host(s)": "Spongey", "Date": "21 Dec. 2019", "Winner": "Flameh"},
           {"Number": "21", "Theme": "Winning is Everything", "Castsize": "21", "Host(s)": "Theb", "Date": "18 Jan. 2020", "Winner": "Dahii"},
           {"Number": "22", "Theme": "Love is Blind", "Castsize": "21", "Host(s)": "Garrett & Keegle", "Date": "8 Feb. 2020", "Winner": "Dahii"},
           {"Number": "23", "Theme": "World War", "Castsize": "20", "Host(s)": "Swishduck & zCent", "Date": "21 Mar. 2020", "Winner": "Bliv"},
           {"Number": "24", "Theme": "Arcade", "Castsize": "20", "Host(s)": "Spongey & Keegle", "Date": "9 May. 2020", "Winner": "zCent"},
           {"Number": "25", "Theme": "Heaven", "Castsize": "18", "Host(s)": "xRoss & Bizzlebub", "Date": "20 Jun. 2020", "Winner": "Tuxpeng"},
           {"Number": "26", "Theme": "Alchemy", "Castsize": "18", "Host(s)": "Keegle", "Date": "14 Aug. 2020", "Winner": "Spongey"},
           {"Number": "27", "Theme": "The Election", "Castsize": "18", "Host(s)": "Theb & Spongey", "Date": "26 Sep. 2020", "Winner": "Purpdan"},
           {"Number": "28", "Theme": "Halloween", "Castsize": "18", "Host(s)": "zCent", "Date": "24 Oct. 2020", "Winner": "CHOCK"},
           {"Number": "29", "Theme": "Avatar 2", "Castsize": "25", "Host(s)": "Spongey & Keegle", "Date": "26 Dec. 2020", "Winner": "CHANGA"},
           {"Number": "30", "Theme": "Legacy", "Castsize": "18", "Host(s)": "Keegle", "Date": "26 Jun. 2021", "Winner": "Swishduck"},
           {"Number": "31", "Theme": "Around the World", "Castsize": "20", "Host(s)": "zCent", "Date": "7 Aug. 2021", "Winner": "Bobby"},
           {"Number": "32", "Theme": "Eden", "Castsize": "18", "Host(s)": "Spongey", "Date": "26 Feb. 2022", "Winner": "SimplySam"},
           {"Number": "33", "Theme": "HvV 2", "Castsize": "18", "Host(s)": "Dahii", "Date": "14 May. 2022", "Winner": "Zeka"},
           {"Number": "34", "Theme": "Pirates Cove", "Castsize": "18", "Host(s)": "Ryfri & Colin", "Date": "1 Apr. 2023", "Winner": "zCent"},
           {"Number": "35", "Theme": "Arcade 2", "Castsize": "20", "Host(s)": "Keegle & Spongey", "Date": "24 Jun. 2023", "Winner": "Miles"},
           {"Number": "36", "Theme": "Spellbound", "Castsize": "18", "Host(s)": "zCent & Swishduck", "Date": "12 Aug. 2023", "Winner": "Bacan"},
           {"Number": "37", "Theme": "Golden Coconut", "Castsize": "20", "Host(s)": "zCent & Swishduck", "Date": "16 Mar. 2024", "Winner": "Type"},
           {"Number": "38", "Theme": "Brains Brawn Beauty", "Castsize": "21", "Host(s)": "zCent", "Date": "22 Jun. 2024", "Winner": "Bobby"},
           {"Number": "39", "Theme": "The Bunker", "Castsize": "18", "Host(s)": "Keegle", "Date": "7 Sep. 2024", "Winner": "Ryfri"},
           {"Number": "40", "Theme": "Calamity", "Castsize": "24", "Host(s)": "Keegle, zCent, and Spongey", "Date": "7 Dec. 2024", "Winner": "Decodin"}]


if not os.path.exists("season_rankings"):
    os.makedirs("season_rankings")

@bot.event
async def on_ready():
    print("Aeonian Bot Online!")
    check_anniversaries.start()


def assign_rank(season_number):
    season_file = f"season_rankings/season_{season_number}.txt"
    
    if not os.path.exists(season_file):
        return None
    
    total_score = 0
    count = 0
    with open(season_file, "r") as file:
        for line in file:
            _, score = line.split()
            total_score += float(score)
            count += 1
    if count == 0:
        return None
    average_score = total_score / count
    return min(10, max(0, average_score)) 

def update_seasons_with_ranks():
    seasons_with_ranks = []
    
    for season in seasons:
        rank = assign_rank(season["Number"])
        season_with_rank = season.copy()
        season_with_rank["rank"] = rank if rank is not None else 0 
        seasons_with_ranks.append(season_with_rank)

    return seasons_with_ranks

seasons_with_ranks = update_seasons_with_ranks()

@bot.event
async def on_message(message):
    if message.channel.name == 'bot' and not message.content.startswith('!') and message.author != bot.user:
        if "survivor" in message.content.lower() or "aeonian" in message.content.lower():
            response = client.chat.completions.create(
                messages=[{"role":"user", "content":f"use this info on seasons: {seasons_with_ranks} and this on player placements: {placementData_tuples} \n{message.content}"}],
                model="gpt-3.5-turbo"
            )
        else:
            response = client.chat.completions.create(
                messages=[{"role":"user", "content":message.content}],
                model="gpt-3.5-turbo"
            )
        chatgpt_reply = response.choices[0].message.content
        await message.channel.send(chatgpt_reply)
    await bot.process_commands(message)

@tasks.loop(hours=24)
async def check_anniversaries():
    today = datetime.datetime.now()
    today = today.strftime("%m-%d")

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%H:%M:%S")
    print(f"Checking dates on: {today} at {formatted_time}")
    for season in seasons:
        date_info = season["Date"]
        date_format = "%d %b. %Y"
        date_object = datetime.datetime.strptime(date_info, date_format)
        numerical_date = date_object.strftime("%m-%d")
        if today == numerical_date:
            channel = discord.utils.get(bot.get_all_channels(), name='general')
            if channel:
                message = f"🎉 Today is the anniversary of Season {season['Number']}: {season['Theme']}!\nIt took place on {season['Date']} and the winner was {season['Winner']}."
                await channel.send(message)



@bot.command(name="predict")
async def predict(ctx, player: str="", vote_predict: int=-1, tribal_predict: int=-1, chal_predict: int=-1):
    if (vote_predict == -1 or tribal_predict == -1 or chal_predict == -1):
        await ctx.send("Correct Usage: !predict <player> <votes_against> <tribals_attended> <challenge_wins>")
        return
    playerIndex = -1
    features = []
    targets = []
    for x in range(len(placementData)):
        if (player.lower() == placementData[x][0].lower()):
            playerIndex = x
            seasonSize = len(placementData[x])
    if (playerIndex != -1):
        placement = [x for x in placementData[playerIndex][1:seasonSize-1] if not pd.isna(x)]
        votes = [x for x in votesrecievedData[playerIndex][1:seasonSize-1] if not pd.isna(x)]
        tribals = [x for x in tribalattendedData[playerIndex][1:seasonSize-1] if not pd.isna(x)]
        chals = [x for x in challengeData[playerIndex][1:seasonSize-1] if not pd.isna(x)]
        
        for x in range(len(placement)):
            features.append([votes[x], tribals[x], chals[x]])
            targets.append(placement[x])
        model = LinearRegression()
        model.fit(features, targets)
        predicted_placement = model.predict([[vote_predict, tribal_predict, chal_predict]])[0]
 
        votes_model = LinearRegression()
        votes_model.fit([[v] for v in votes], targets)
        votes_r2 = votes_model.score([[v] for v in votes], targets)
        
        tribals_model = LinearRegression()
        tribals_model.fit([[t] for t in tribals], targets)
        tribals_r2 = tribals_model.score([[t] for t in tribals], targets)
        
        chals_model = LinearRegression()
        chals_model.fit([[c] for c in chals], targets)
        chals_r2 = chals_model.score([[c] for c in chals], targets)

        ranking_msg = ""
        if (votes_r2 > chals_r2 and votes_r2 > tribals_r2):
            ranking_msg += "Votes Against,"
            if (chals_r2 > tribals_r2):
                ranking_msg += " Challenge Wins, and"
                ranking_msg += " Tribals Attended"
            else:
                ranking_msg += " Tribals Attended, and"
                ranking_msg += " Challenge Wins"
        elif (chals_r2 > votes_r2 and chals_r2 > tribals_r2):
            ranking_msg += "Challenge Wins,"
            if (votes_r2 > tribals_r2):
                ranking_msg += " Votes Against, and"
                ranking_msg += " Tribals Attended"
            else:
                ranking_msg += " Tribals Attended, and"
                ranking_msg += " Votes Against"
        else:
            ranking_msg += "Tribals Attended,"
            if (votes_r2 > chals_r2):
                ranking_msg += " Votes Against, and"
                ranking_msg += " Challenge Wins"
            else:
                ranking_msg += " Challenge Wins, and"
                ranking_msg += " Votes Against"
        await ctx.send(f"{ctx.author.mention} Predicted placement for {player} based on those numbers is: {predicted_placement:.2f}\nThe factors that contribute most to this player's place from most to least are: {ranking_msg}")
    else:
        await ctx.send("Couldn't find that player, do !listplayers to see a list of everyone who has played Aeonian!")

@bot.command(name="listplayers", brief='Lists all people who have played Aeonian Survivor', description='Lists all people who have played Aeonian Survivor')
async def listplayers(ctx):
    await ctx.send(f"{ctx.author.mention} {playerList}")

@bot.command(name="top", brief='Lists top amount of players for a category with an amount of seasons played as the cutoff', description='Lists top amount of players for a category with an amount of seasons played as the cutoff')
async def top(ctx, category: str="dumb", amount: int=10, cutoff: int=5):
    if (category == "dumb"):
        await ctx.send(f"{ctx.author.mention} Invalid category. Please choose from: placement, challenge_wins, tribals_attended, votes_for. Full command usage: top <category> <amount> <cutoff>")
        return
    amount = min(amount, len(playerList))
    category_data = {
        "placement": placementData,
        "challenge_wins": challengeData,
        "tribals_attended": tribalattendedData,
        "votes_for": votesrecievedData
    }
    if category not in category_data:
        await ctx.send(f"{ctx.author.mention} Invalid category. Please choose from: placement, challenge_wins, tribals_attended, votes_for.")
        return
    data = category_data[category]
    rankings = []
    for i, player in enumerate(playerList):
        seasons_played = len([x for x in placementData[i][1:] if not pd.isna(x)]) - 1
        if seasons_played < cutoff:
            continue
        if not pd.isna(data[i][-1]):
            average_score = data[i][-1]
            rankings.append((player, average_score))
    if category == "placement":
        rankings.sort(key=lambda x: x[1])
    else:
        rankings.sort(key=lambda x: x[1], reverse=True)
    top_players = rankings[:amount]
    top_players_msg = '\n'.join([f"{i+1}. {player} » {average_score:.2f}" 
                                 for i, (player, average_score) in enumerate(top_players)])
    await ctx.send(f"{ctx.author.mention} Here are the top {amount} players based on the AVERAGE for {category} that have played at least {cutoff} seasons:\n\n{top_players_msg}")

@bot.command(name="playerinfo", brief='Lists all info of a specific player !playerinfo <player>', description='Lists all info of a specific player !playerinfo <player>')
async def playerinfo(ctx, player: str):
    playerIndexPlace = -1
    for x in range(len(placementData)):
        if (player.lower() == placementData[x][0].lower()):
            playerIndexPlace = x
            seasonSizePlace = len(placementData[x])
    for x in range(len(votesrecievedData)):
        if (player.lower() == votesrecievedData[x][0].lower()):
            playerIndexVote = x
            seasonSizeVote = len(votesrecievedData[x])
    for x in range(len(tribalattendedData)):
        if (player.lower() == tribalattendedData[x][0].lower()):
            playerIndexTribal = x
            seasonSizeTribal = len(tribalattendedData[x])
    for x in range(len(challengeData)):
        if (player.lower() == challengeData[x][0].lower()):
            playerIndexChal = x
            seasonSizeChal = len(challengeData[x])
    if (playerIndexPlace != -1):
        placement = placementData[playerIndexPlace][seasonSizePlace-1]
        avgvotes = votesrecievedData[playerIndexVote][seasonSizeVote-1]
        totvotes = votesrecievedData[playerIndexVote][seasonSizeVote-2]
        avgtribals = tribalattendedData[playerIndexTribal][seasonSizeTribal-1]
        tottribals = tribalattendedData[playerIndexTribal][seasonSizeTribal-2]
        avgchals = challengeData[playerIndexChal][seasonSizeChal-1]
        totchals = challengeData[playerIndexChal][seasonSizeChal-2]
        totseasons = len([x for x in placementData[playerIndexPlace] if not pd.isna(x)])-2

        emb_msg = discord.Embed(title="Player Info", color=discord.Color.random())
        emb_msg.set_thumbnail(url=ctx.guild.icon)
        emb_msg.add_field(name=f"{player}:", value=f"Seasons Played: {totseasons:.1f}\nAVG Placement: {placement:.1f}\nAVG Votes Recieved: {avgvotes:.1f}\nTOT Votes Recieved: {totvotes:.1f}\nAVG Tribals: {avgtribals:.1f}\nTOT Tribals: {tottribals:.1f}\nAVG Chals: {avgchals:.1f}\nTOT Chals: {totchals:.1f}", inline=False)
        keegle_avatar_url = get_keegle_avatar(ctx)
        if keegle_avatar_url:
            emb_msg.set_footer(text='Bot coded by Keegle in Python!', icon_url=keegle_avatar_url)
        else:
            emb_msg.set_footer(text='Bot coded by Keegle in Python!')
        await ctx.send(embed=emb_msg)
    else:
        await ctx.send("Couldn't find that player, do !listplayers to see a list of everyone who has played Aeonian!")


@bot.command(name="rank", brief='Rank a season out of 10 !rank <season_num> <rank>', description='Rank a season out of 10 !rank <season_num> <rank>')
async def rank(ctx, season: int = -1, score: float = -1):
    if season == -1 or score == -1:
        await ctx.send("Correct Usage: !rank <season> <score>")
        return
    
    if not (1 <= score <= 10):
        await ctx.send(f"{ctx.author.mention}, please provide a score between 1 and 10.")
        return
    
    username = str(ctx.author)
    season_file = f"season_rankings/season_{season}.txt"
    new_rankings = []
    user_found = False

    if os.path.exists(season_file):
        with open(season_file, "r") as file:
            for line in file:
                if line.startswith(username):
                    new_rankings.append(f"{username} {score}\n")
                    user_found = True
                else:
                    new_rankings.append(line)
    
    if not user_found:
        new_rankings.append(f"{username} {score}\n")

    with open(season_file, "w") as file:
        file.writelines(new_rankings)
    
    await ctx.send(f"{ctx.author.mention}, you ranked season {season} a {score}/10.")


@bot.command(name="season", brief='Give all info about a season !season <season_num>', description='Give all info about a season !season <season_num>')
async def season(ctx, season: int = -1):
    if season == -1:
        await ctx.send("Provide a season!")
        return
    elif season < 1 or season > 40:
        await ctx.send("Provide a season that's happened!")
        return

    season_file = f"season_rankings/season_{season}.txt"
    
    if not os.path.exists(season_file):
        await ctx.send(f"{ctx.author.mention}, no rankings found for season {season}.")
        return
    
    total_score = 0
    count = 0
    
    with open(season_file, "r") as file:
        for line in file:
            _, score = line.split()
            total_score += float(score)
            count += 1
    
    emb_msg = discord.Embed(title="Season Info", color=discord.Color.random())
    emb_msg.set_thumbnail(url=ctx.guild.icon)
    if count == 0:
        emb_msg.add_field(name=f"Season: {season}", value=f"Theme: {seasons[season-1]['Theme']}\nWinner: {seasons[season-1]['Winner']}\nHost(s): {seasons[season-1]['Host(s)']}\nDate: {seasons[season-1]['Date']}\nCastsize: {seasons[season-1]['Castsize']}", inline=False)
    else:
        average_score = total_score / count
        emb_msg.add_field(name=f"Season: {season}", value=f"Theme: {seasons[season-1]['Theme']}\nWinner: {seasons[season-1]['Winner']}\nHost(s): {seasons[season-1]['Host(s)']}\nDate: {seasons[season-1]['Date']}\nCastsize: {seasons[season-1]['Castsize']}\nRanking: {average_score:.1f}", inline=False)

    keegle_avatar_url = get_keegle_avatar(ctx)
    if keegle_avatar_url:
        emb_msg.set_footer(text='Bot coded by Keegle in Python!', icon_url=keegle_avatar_url)
    else:
        emb_msg.set_footer(text='Bot coded by Keegle in Python!')
    await ctx.send(embed=emb_msg)

@bot.command(name="seasonorder", brief='Orders all seasons by rank', description='Orders all seasons by rank')
async def seasonorder(ctx):
    rankings = []
    
    for season_file in os.listdir("season_rankings"):
        if season_file.startswith("season_") and season_file.endswith(".txt"):
            season_number = int(season_file.split("_")[1].split(".")[0])
            total_score = 0
            count = 0
            
            with open(f"season_rankings/{season_file}", "r") as file:
                for line in file:
                    _, score = line.split()
                    total_score += float(score)
                    count += 1
            
            if count > 0:
                average_score = total_score / count
                rankings.append((season_number, average_score))
    
    rankings.sort(key=lambda x: x[1], reverse=True)
    
    rank_message = ""
    for rank, (season, score) in enumerate(rankings, 1):
        rank_message += f"{rank}. {seasons[season-1]['Theme']} ({season}): {score:.1f}/10\n"
    
    await ctx.send(f"{ctx.author.mention} Ordered Seasons (Best to Worst): \n{rank_message}")

@bot.command(name="myrankings", brief='Lists all your rankings', description='Lists all your rankings')
async def myrankings(ctx):
    username = str(ctx.author)
    user_rankings = []
    
    for season_file in os.listdir("season_rankings"):
        if season_file.startswith("season_") and season_file.endswith(".txt"):
            season_number = int(season_file.split("_")[1].split(".")[0])
            
            with open(f"season_rankings/{season_file}", "r") as file:
                for line in file:
                    user, score = line.split()
                    if user == username:
                        user_rankings.append((season_number, float(score)))
    
    if not user_rankings:
        await ctx.send(f"{ctx.author.mention}, you have not ranked any seasons yet.")
        return
    
    user_rankings.sort(key=lambda x: x[0])
    
    rank_message = f"{ctx.author.mention}, your rankings:\n"
    for season, score in user_rankings:
        rank_message += f"Season {season}: {score}/10\n"
    
    await ctx.send(rank_message)

def get_keegle_avatar(ctx):
    # Search for 'keegle' in the members of the guild
    for member in ctx.guild.members:
        if member.name == 'keegle':
            return member.avatar.url
    return None

with open("token.txt") as file:
    token = file.read()

bot.run(token)

