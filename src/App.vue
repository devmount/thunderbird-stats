<template>
	<div id="app">
		in: {{ figure.in }}
		out: {{ figure.out }}
		total: {{ figure.total }}
		<LineChart title="Mails per Year" :datasets="mailsPerYear.datasets" :labels="mailsPerYear.labels" />
		<LineChart title="Mails per Month" :datasets="mailsPerMonth.datasets" :labels="mailsPerMonth.labels" />
		<LineChart title="Mails per Daytime" :datasets="mailsPerHour.datasets" :labels="mailsPerHour.labels" />
		<LineChart title="Mails per Weekday" :datasets="mailsPerWeekday.datasets" :labels="mailsPerWeekday.labels" />
	</div>
</template>

<script>
// internal components
import LineChart from './components/LineChart.vue'

// chart data
import MAILS_PER_HOUR from './data/mails-per-hour.json'
import MAILS_PER_MONTH from './data/mails-per-month.json'
import MAILS_PER_YEAR from './data/mails-per-year.json'
import MAILS_PER_WEEKDAY from './data/mails-per-weekday.json'

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
		mailsPerWeekday: MAILS_PER_WEEKDAY,
	},
	computed: {
		figure () {
			var din = Object.values(this.$options.stats.mailsPerYear.in).reduce( (a, c) => a + c, 0 )
			var dout = Object.values(this.$options.stats.mailsPerYear.out).reduce( (a, c) => a + c, 0 )
			return {
				in: din,
				out: dout,
				total: din + dout
			}
		},
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
					{ label: 'Outgoing', data: dsout, color: 'rgb(237, 47, 71)', bcolor: 'rgb(237, 47, 71, .2)'  },
					{ label: 'Incoming', data: dsin,  color: 'rgb(48, 206, 242)', bcolor: 'rgb(48, 206, 242, .2)' },
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
					if(dout.hasOwnProperty(year) && dout[year].hasOwnProperty(month)) {
						dsout.push(dout[year][month])
					} else {
						dsout.push(0)
					}
				}
			}
			return {
				datasets: [
					{ label: 'Outgoing', data: dsout, color: 'rgb(237, 47, 71)', bcolor: 'rgb(237, 47, 71, .2)'  },
					{ label: 'Incoming', data: dsin,  color: 'rgb(48, 206, 242)', bcolor: 'rgb(48, 206, 242, .2)' },
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
					{ label: 'Outgoing', data: dsout, color: 'rgb(237, 47, 71)', bcolor: 'rgb(237, 47, 71, .2)'  },
					{ label: 'Incoming', data: dsin,  color: 'rgb(48, 206, 242)', bcolor: 'rgb(48, 206, 242, .2)' },
				],
				labels: hours
			}
		},
		mailsPerWeekday () {
			var din = this.$options.stats.mailsPerWeekday.in
			var dout = this.$options.stats.mailsPerWeekday.out
			var weekdays = [], dsin = [], dsout = []
			var days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
			for (const weekday in din) {
				weekdays.push(days[weekday])
				dsin.push(din[weekday])
				dsout.push(dout[weekday])
			}
			return {
				datasets: [
					{ label: 'Outgoing', data: dsout, color: 'rgb(237, 47, 71)', bcolor: 'rgb(237, 47, 71, .2)'  },
					{ label: 'Incoming', data: dsin,  color: 'rgb(48, 206, 242)', bcolor: 'rgb(48, 206, 242, .2)' },
				],
				labels: weekdays
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
	width 960px
</style>
