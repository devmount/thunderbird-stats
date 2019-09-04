<template>
	<div id="app">
		<LineChart title="Mails per Year" :datasets="mailsPerYear.datasets" :labels="mailsPerYear.labels" />
		<LineChart title="Mails per Month" :datasets="mailsPerMonth.datasets" :labels="mailsPerMonth.labels" />
		<LineChart title="Mails per Daytime" :datasets="mailsPerHour.datasets" :labels="mailsPerHour.labels" />
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
					{ label: 'Incoming', data: dsin,  color: 'rgb(48, 206, 242)' },
					{ label: 'Outgoing', data: dsout, color: 'rgb(237, 47, 71)'  }
				],
				labels: years
			}
		},
		mailsPerMonth () {
			var din = this.$options.stats.mailsPerMonth.in
			var dout = this.$options.stats.mailsPerMonth.out
			var months = [], dsin = [], dsout = []
			for (const year in din) {
				for (const month in din[year]) {
					months.push(year + '-' + month)
					dsin.push(din[year][month])
					dsout.push(dout[year][month])
				}
			}
			return {
				datasets: [
					{ label: 'Incoming', data: dsin,  color: 'rgb(48, 206, 242)' },
					{ label: 'Outgoing', data: dsout, color: 'rgb(237, 47, 71)'  }
				],
				labels: months
			}
		},
		mailsPerHour () {
			var din = this.$options.stats.mailsPerHour.in
			var dout = this.$options.stats.mailsPerHour.out
			var hours = [], dsin = [], dsout = []
			for (const hour in din) {
				hours.push(hour)
				dsin.push(din[hour])
				dsout.push(dout[hour])
			}
			return {
				datasets: [
					{ label: 'Incoming', data: dsin,  color: 'rgb(48, 206, 242)' },
					{ label: 'Outgoing', data: dsout, color: 'rgb(237, 47, 71)'  }
				],
				labels: hours
			}
		},
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
	margin 20px auto 0 auto
	width 600px
</style>
