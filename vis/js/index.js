var data = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
        {
            label: "My First dataset",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: [65, 59, 80, 81, 56, 55, 40]
        },
        {
            label: "My Second dataset",
            fillColor: "rgba(151,187,205,0.2)",
            strokeColor: "rgba(151,187,205,1)",
            pointColor: "rgba(151,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(151,187,205,1)",
            data: [28, 48, 40, 19, 86, 27, 90]
        }
    ]
};



// SEARCH BAR VARS
var teams
var teamNames
// var teamIDs
var players
var playerNames
// var playerIDs
var selectables

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
        // teamIDs.push(team)
    };

    players = mappings["players"];
    playerNames = []
    playerIDs = []
    for (player in players) {
        playerNames.push({'value':players[player]['player_name'], 'data':player})
        // playerIDs.push(player)
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

// function called when elem is clicked to make items selectable
function addSelectable(elem) {
    if (elem.classList.contains("selected")){
        elem.classList.remove("selected");
    }
    else {
        elem.classList.add("selected");
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
function sAddSelectable(elem) {
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




window.onload = function() {
    // CHART STUFF
    var ctx = document.getElementById("myChart").getContext("2d");
    var myNewChart = new Chart(ctx).Line(data);

    // MAKE ITEMS SELECTABLE
    // makeSelectable();

    // SEARCH BAR STUFF
    setNames();

    $('#autocomplete').autocomplete({
        lookup: determineLookup(),
        onSelect: function (suggestion) {
            alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
        }
    });

};

























