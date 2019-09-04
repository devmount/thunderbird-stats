<template>
	<div id="app">
		<LineChart title="Mails per Year" :datasets="mailsPerYear.datasets" :labels="mailsPerYear.labels" />
	</div>
</template>

<script>
// internal components
import LineChart from './components/LineChart.vue'

// chart data
import MAILS_PER_HOUR from './data/mails-per-hour.json'
import MAILS_PER_MONTH from './data/mails-per-month.json'
import MAILS_PER_YEAR from './data/mails-per-year.json'

// initialize Chart.js default options
import Chart from 'chart.js'
Chart.defaults.global.elements.arc.borderWidth = 0;
Chart.defaults.global.legend.display = false;

export default {
	name: 'app',
	components: {
		LineChart
	},
	stats: {
		mailsPerHour: MAILS_PER_HOUR,
		mailsPerMonth: MAILS_PER_MONTH,
		mailsPerYear: MAILS_PER_YEAR,
	},
	computed: {
		mailsPerYear () {
			var din = this.$options.stats.mailsPerYear.in
			var dout = this.$options.stats.mailsPerYear.out
			var years = [], dsin = [], dsout = []
			for (const year in din) {
				years.push(year)
				dsin.push(din[year])
				dsout.push(dout[year])
			}
			return {
				datasets: [
					{ data: dsin,  color: 'rgb(48, 206, 242)' },
					{ data: dsout, color: 'rgb(237, 47, 71)'  }
				],
				labels: years
			}
		}
	},
}
</script>
<style lang="stylus">
#app
	font-family 'Avenir', Helvetica, Arial, sans-serif
	-webkit-font-smoothing antialiased
	-moz-osx-font-smoothing grayscale
	text-align center
	color #2c3e50
	margin-top 60px
</style>
