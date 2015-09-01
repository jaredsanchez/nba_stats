google.load("visualization", "1", {packages:["corechart"]});

var chart;
var statsObj;
var currSeason;
var games;
var newRow;
var data;
var dateHelp;
// var lossIndexes = [];
// var svg;
// var points;

function clearPlot() {
	chart.clearChart();
}

// function that checks to make sure all the fields are correct
function isPlotReady() {
	if (playerOrTeam === 'teams' && statsSelected.indexOf("SPD") !== -1) {
		alert("Sorry! There are no speed statistics kept on teams");
		return false;
	}
	if (ptID === undefined) {
		alert("You need to select a team/player");
		return false;
	}
	if (statsSelected.length === 0) {
		alert("You need to select stats to plot");
		return false
	}
	return true
}

function drawPlot() {
	// check that all the necessary fields are filled in
	if (!isPlotReady()) {
		return
	}
	// clear the existing plot
	if (chart !== undefined) {
		clearPlot();
	}
	// run function to set selected seasons var
	genSelectedSeasons();

	statsObj = visData[playerOrTeam][ptID];
	data = new google.visualization.DataTable();

	// add date column to DataTable
	data.addColumn('date', 'Date');
	// add custom tooltip column
	data.addColumn({'type': 'string', 'role': 'tooltip', 'p': {'html': true}})
	
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
        	dateHelp = currSeason[games[k]]['date'].split('-'); // do some stupid js stuff to get the date correct 
        	newRow = [new Date(Date.UTC(dateHelp[0], (parseInt(dateHelp[1])-1).toString(), (parseInt(dateHelp[2])+1).toString()))]; // do some stupid js stuff to get the date correct 
        	// create tooltip with date and opponent
        	newRow.push(customToolTip(newRow[0], currSeason[games[k]]));

        	// iterate through all selected stats, adding each for the curr game to the new row
            for (var i=0; i<statsSelected.length; i++) {
            	newRow.push(currSeason[games[k]]['stats'][statsSelected[i]]); // add the stat
            	// add the appropriate point customization for win or loss
            	if (currSeason[games[k]]['win_or_loss'] === 'Loss') {
            		newRow.push('point {fill-color:#f44336}');
            	} else {
            		newRow.push('point {fill-color:#4caf50}');
            	}
            	// add custom tool tip for each stat
            	if (currSeason[games[k]]['stats'][statsSelected[i]] === null || currSeason[games[k]]['stats'][statsSelected[i]] === undefined) {
            		newRow[1] = newRow[1].concat(customToolTipPart2(statsSelected[i], '', i));
            	} else {
            		newRow[1] = newRow[1].concat(customToolTipPart2(statsSelected[i], currSeason[games[k]]['stats'][statsSelected[i]].toString(), i));
           		}
            }
        	// add the closing tag of the tool tip div
        	newRow[1] = newRow[1].concat('</div');
            data.addRows([newRow]);
        }
    }

    var options = {
        // title: 'Stats Analysis',
        legend: {position: 'right'}, 
        backgroundColor: '#FAFAFA',
        pointSize: 3,
        focusTarget: 'category',
        tooltip: {isHtml: true},
        animation: {startup: true, duration: 2000, easing: 'out'},
        colors: ['#2196f3', '#ffc107', '#9c27b0', '#cddc39', '#009688'],
		trendlines: addTrendLines(),
    };

    chart = new google.visualization.LineChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

// function to generate html for the first part of the plot tooltips (Date, Opponent, Outcome)
function customToolTip(date, game) {
	return '<div id="plot-tool-tip">' +
				'<div class="bold">' + date.toString().substring(0,15) + '</div>' + // date
				'<div>' + 'Opponent: ' + '<span class="bold">' + game['opponent'] + '</span></div>' + // opponent
				'<div>' + 'Outcome: ' + '<span class="bold">' + game['win_or_loss'] + '</span></div>' // outcome of game
}

// function to generate html for the second part of the plot tooltips (all the stats and their values)
function customToolTipPart2(stat, value, i) {
	switch (i) {
		case 0:
			return '<div>' + 
					'<span class="box zero"></span>' + // box color
					'<span>' + stat + ': ' + // stat name
						 '<span class="bold">' + value + '</span>' + // stat value
					'</span>' +
				'</div>'
		case 1:
			return '<div>' + 
					'<span class="box one"></span>' + // box color
					'<span>' + stat + ': ' + // stat name
						 '<span class="bold">' + value + '</span>' + // stat value
					'</span>' +
				'</div>'
		case 2:
			return '<div>' + 
					'<span class="box two"></span>' + // box color
					'<span>' + stat + ': ' + // stat name
						 '<span class="bold">' + value + '</span>' + // stat value
					'</span>' +
				'</div>'
		case 3: 
			return '<div>' + 
					'<span class="box three"></span>' + // box color
					'<span>' + stat + ': ' + // stat name
						 '<span class="bold">' + value + '</span>' + // stat value
					'</span>' +
				'</div>'
		case 4:
			return '<div>' + 
					'<span class="box four"></span>' + // box color
					'<span>' + stat + ': ' + // stat name
						 '<span class="bold">' + value + '</span>' + // stat value
					'</span>' +
				'</div>'
	} 
}

// function to return the appropriate trendLines object to pass as an option to the chart
function addTrendLines() {
	if (document.getElementById('trend-lines').checked === true) {
		return {
			0: {
				type: 'linear',
	    		visibleInLegend: true,
	    		opacity: 0.5,
	    		pointsVisible: false,
	    		showR2: true,
	    		labelInLegend: statsSelected[0] + ' Trend Line',},
			1: {
				type: 'linear',
	    		visibleInLegend: true,
	    		opacity: 0.5,
	    		pointsVisible: false,
	    		showR2: true,
	    		labelInLegend: statsSelected[1] + ' Trend Line',},
			2: {
				type: 'linear',
	    		visibleInLegend: true,
	    		opacity: 0.5,
	    		pointsVisible: false,
	    		showR2: true,
	    		labelInLegend: statsSelected[2] + ' Trend Line',},
			3: {
				type: 'linear',
	    		visibleInLegend: true,
	    		opacity: 0.5,
	    		pointsVisible: false,
	    		showR2: true,
	    		labelInLegend: statsSelected[3] + ' Trend Line',},
			4: {
				type: 'linear',
	    		visibleInLegend: true,
	    		opacity: 0.5,
	    		pointsVisible: false,
	    		showR2: true,
	    		labelInLegend: statsSelected[4] + ' Trend Line',},
		}
	}
	return null
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







