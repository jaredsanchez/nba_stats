var myLineChart;
var ctx;

// SEARCH BAR VARS
var teams;
var teamNames;
var players;
var playerNames;
var selectables;

var statsSelected = [];
var seasonsSelected;
var playerOrTeam;
var ptID;


function getChildren(n, skipMe){
    var r = [];
    for ( ; n; n = n.nextSibling ) 
       if ( n.nodeType == 1 && n != skipMe)
          r.push( n );        
    return r;
};
function getSiblings(n) {
    return getChildren(n.parentNode.firstChild, n);
}


// Function to create arrays for search bar lookup
function setNames() {
    teams = mappings["teams"];
    teamNames = [];
    teamIDs = [];
    for (team in teams) {
        teamNames.push({'value':teams[team]['team_city']+' '+teams[team]['team_name'], 'data': team})
    };

    players = mappings["players"];
    playerNames = []
    playerIDs = []
    for (player in players) {
        playerNames.push({'value':players[player]['player_name'], 'data':player})
    };
}

// function to determine if search bar should use team or player array
function determineLookup() {
    if (document.getElementById("teams").classList.contains('selected')) {
        return teamNames
    }
    else if (document.getElementById("players").classList.contains('selected')) {
        return playerNames
    }
    else {
        return []
    }
}

// function called handle adding selected class to stat fields
function addSelectable(elem) {
    if (elem.classList.contains("selected")){
        elem.classList.remove("selected");
        var index = statsSelected.indexOf(elem.dataset.stat);
        statsSelected.splice(index, 1);
    }
    else {
        if (statsSelected.length < 5) {
            elem.classList.add("selected");
            statsSelected.push(elem.dataset.stat);
        } else {
            alert("You can only plot at most 5 stats!");
        }
    }
}

// function to handle adding selected class to team/player
function tpAddSelectable(elem) {
    if (elem.id === 'teams') {
        if (elem.classList.contains("selected")){
            return
        }
        else {
            elem.classList.add("selected");
            elem.nextElementSibling.classList.remove("selected");
            $('#autocomplete').autocomplete().setOptions({'lookup': determineLookup()});
        }
    } else {
        if (elem.classList.contains("selected")){
            return
        }
        else {
            elem.classList.add("selected");
            elem.previousElementSibling.classList.remove("selected");
            $('#autocomplete').autocomplete().setOptions({'lookup': determineLookup()});
        }
    }
}

// function to handle adding selected class to seasons
function seasonAddSelectable(elem) {
    if (elem.id === 'all') {
        if (elem.classList.contains("selected")){
            return
        } else {
            elem.classList.add("selected");
            var nextElem = elem.nextElementSibling;
            while (nextElem !== null) {
                nextElem.classList.remove("selected");
                nextElem = nextElem.nextElementSibling;
            }
        }
    } else {
        if (elem.classList.contains("selected")){
            var siblings = getSiblings(elem);
            for (var i=0; i<siblings.length; i++) {
                if (siblings[i].classList.contains("selected")) {
                    elem.classList.remove("selected");
                    return;
                }
            }
        } else {
            elem.classList.add("selected");
            if (document.getElementById("all").classList.contains("selected")) {
                document.getElementById("all").classList.remove("selected")
            }
        }
    }
}

// function to populate selecetedSeasons var with all the seasons
function genSelectedSeasons() {
    seasonsSelected = [];
    var allElem = document.getElementById('all');
    var nextYear = allElem.nextElementSibling;
    if (allElem.classList.contains('selected')) {
        while (nextYear!=null) {
            seasonsSelected.push(nextYear.innerHTML);
            nextYear = nextYear.nextElementSibling;
        }
    } else {
        while (nextYear!=null) {
            if (nextYear.classList.contains('selected')) {
                seasonsSelected.push(nextYear.innerHTML);
            }
            nextYear = nextYear.nextElementSibling;
        }
    }
}





window.onload = function() {
    // CHART STUFF
    // ctx = document.getElementById("myChart").getContext("2d");
    // myLineChart = new Chart(ctx).Line(data);

    // SEARCH BAR STUFF
    setNames();

    $('#autocomplete').autocomplete({
        lookup: determineLookup(),
        onSelect: function (suggestion) {
            // alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
            ptID = suggestion.data;
            if (document.getElementById('teams').classList.contains("selected")){
                playerOrTeam = "teams";
            } else {
                playerOrTeam = "players";
            }
        }
    });

};

























