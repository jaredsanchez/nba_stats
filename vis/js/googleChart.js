google.load("visualization", "1", {packages:["corechart"]});

var chart;
var statsObj;
var currSeason;
var games;
var newRow;
var data;
// var lossIndexes = [];
// var svg;
// var points;

function clearPlot() {
	chart.clearChart();
}

function drawPlot() {
	if (chart !== undefined) {
		clearPlot();
	}
	// run function to set selected seasons var
	genSelectedSeasons();

	statsObj = visData[playerOrTeam][ptID];
	data = new google.visualization.DataTable();

	// add date column to DataTable
	data.addColumn('date', 'Date');
	
	// add all selected stats as columns in DataTable
	for (var i=0; i<statsSelected.length; i++) {
		data.addColumn('number', statsSelected[i]);
		// add column for point customizations
		data.addColumn({'type': 'string', 'role': 'style'});
	}

	// add all the rows to the DataTable
	for (var j=0; j<seasonsSelected.length; j++) {
        currSeason = statsObj[seasonsSelected[j]]; //set currSeason
        games = Object.keys(currSeason).sort(); // get game id's from currSeason and sort so they are in order
        // iterate through all the games
        for (var k=0; k<games.length; k++) {
        	// create a new row with current game date
        	newRow = [new Date(currSeason[games[k]]['date'])];
            // check if current game is a win or loss
        	if (currSeason[games[k]]['win_or_loss'] === 'Loss') {
        		// iterate through all selected stats, adding each for the curr game to the new row
	            for (var i=0; i<statsSelected.length; i++) {
	            	newRow.push(currSeason[games[k]]['stats'][statsSelected[i]]); // add the stat
	            	newRow.push('point {fill-color:#f44336}'); // add the appropriate point customization
	            }
        	} else {
        		// iterate through all selected stats, adding each for the curr game to the new row
	            for (var i=0; i<statsSelected.length; i++) {
	            	newRow.push(currSeason[games[k]]['stats'][statsSelected[i]]); // add the stat
	            	newRow.push('point {fill-color:#4caf50}'); // add the appropriate point customization
	            }
        	}
            data.addRows([newRow]);
        }
    }

    var options = {
        // title: 'Stats Analysis',
        // curveType: 'function',
        // hAxis: {title: 'Date', minValue: 0, maxValue: data.Gf.length},
        // vAxis: {title: 'Stat Values', minValue: 0, maxValue: 100},
        legend: {position: 'right'}, 
        backgroundColor: '#FAFAFA',
        // explorer: {},
        pointSize: 3,
        focusTarget: 'category',
        // tooltip: {isHtml: true},
        animation: {startup: true, duration: 2000, easing: 'out'},
        colors: ['#2196f3', '#ffc107', '#9c27b0', '#cddc39', '#009688'],
  //       trendlines: {
		//     0: {
		//       type: 'linear',
		//       color: '#2196f3',
		//       lineWidth: 3,
		//       opacity: 0.3,
		//       showR2: true,
		//       visibleInLegend: true
		//     }
		// }
		// series: {
		// 	0: {},
		// 	1: {},
		// 	2: {},
		// 	3: {},
		// 	4: {},
		// },
		trendlines: {
			0: {
				type: 'linear',
        		visibleInLegend: true,
			},
			1: {
				type: 'linear',
        		visibleInLegend: true,
			},
			2: {
				type: 'linear',
        		visibleInLegend: true,
			},
			3: {
				type: 'linear',
        		visibleInLegend: true,
			},
			4: {
				type: 'linear',
        		visibleInLegend: true,
			},
		}
    };

    chart = new google.visualization.LineChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}



// // // 
// // // // KEEP THIS FOR REFERENCE
// // // 
// function markLosses() {
// 	svg = document.getElementsByTagName('svg'); // get the svg element
// 	// console.log(svg);
// 	points = svg[0].children[4].children[2].children; // get all the points on the plot

// 	var gameNum = 0;
// 	var currLossIndex = 0;
// 	var indexOfNextLoss = lossIndexes[currLossIndex];

// 	for (var i=0; i<points.length; i++) {
// 		// reset gameNum after x num of games to account for each stat
// 		if (gameNum === 82*seasonsSelected.length) {
// 			gameNum = 0;
// 		}
// 		// reset currLossIndex after completing a stat
// 		if (currLossIndex === lossIndexes.length) {
// 			currLossIndex = 0;
// 			indexOfNextLoss = lossIndexes[currLossIndex];
// 		}
// 		// if curr game is a loss
// 		if (gameNum === indexOfNextLoss) {
// 			// points[i].style.fill = '#FF4545'; // red
// 			// points[i].setAttribute('fill', '#FF4545');
// 			points[i].classList.add('loss');
// 			// points[i].style.opacity = 0;
// 			currLossIndex++; // increment lossIndex
// 			indexOfNextLoss = lossIndexes[currLossIndex]; // get next lossIndex
// 		// if curr game is a win
// 		} else {
// 			// points[i].style.fill = '#59D659'; //green
// 			points[i].setAttribute('fill', '#59D659');
// 		}
// 		gameNum++;
// 	}


// }







