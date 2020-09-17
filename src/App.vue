<template>
	<div id="app">
		<div class="container grid-lg">
			<div class="columns mt-1-5">
				<!-- title -->
				<div class="column col-8 col-md-12">
					<h1 class="text-left">Thunderbird Email Stats</h1>
				</div>
				<div class="column col-4 col-md-12">
					<select v-model="view" class="form-select">
						<option v-for="(a,i) in addresses" :key="i" :value="a">{{ a }}</option>
					</select>
				</div>
			</div>
			<div class="columns mt-1">
				<!-- featured figures -->
				<div class="column col-2 col-md-3 col-sm-6 text-center">
					<div class="text-gray">Mails total</div>
					<div class="figure">{{ figure.total }}</div>
					<div class="text-gray">within {{ figure.years }} years</div>
				</div>
				<div class="column col-2 col-md-3 col-sm-6 text-center">
					<div class="text-gray">Mails unread</div>
					<div class="figure" v-if="view == 'total'">{{ figure.unread }}</div>
					<div class="figure" v-else>n.a.</div>
					<div class="text-gray" v-if="figure.unread > 0">{{ figure.unreadPercentage }}% of total</div>
					<div class="text-gray" v-else-if="view == 'total'">Nice work!</div>
				</div>
				<div class="column col-2 col-md-3 col-sm-6 text-center">
					<div class="text-primary">Mails received</div>
					<div class="figure text-primary">{{ figure.in }}</div>
					<div class="text-gray">{{ figure.inPercentage }}% of total</div>
				</div>
				<div class="column col-2 col-md-3 col-sm-6 text-center">
					<div class="text-secondary">Mails sent</div>
					<div class="figure text-secondary">{{ figure.out }}</div>
					<div class="text-gray">{{ figure.outPercentage }}% of total</div>
				</div>
				<div class="column col-2 col-md-3 col-sm-6 text-center">
					<div class="text-gray">Mails per month</div>
					<div class="figure">{{ figure.permonth }}</div>
					<div class="text-gray">{{ figure.peryear }} mails/year</div>
				</div>
				<div class="column col-2 col-md-3 col-sm-6 text-center">
					<div class="text-gray">Mails per day</div>
					<div class="figure">{{ figure.perday }}</div>
					<div class="text-gray">{{ figure.perweek }} mails/week</div>
				</div>
			</div>
			<!-- line charts for mail amount per year and month -->
			<div class="columns mt-1-5">
				<div class="column col-6 col-sm-12">
					<LineChart
						title="Years"
						description="Total number of emails per year"
						:datasets="mailsPerYear.datasets"
						:labels="mailsPerYear.labels"
					/>
				</div>
				<div class="column col-6 col-sm-12">
					<LineChart
						title="Months"
						description="Total number of emails per month"
						:datasets="mailsPerMonth.datasets"
						:labels="mailsPerMonth.labels"
					/>
				</div>
			</div>
			<!-- bar charts for mail distribution over daytime and weekday -->
			<div class="columns mt-1-5">
				<div class="column col-6 col-sm-12">
					<BarChart
						title="Daytime"
						description="Number of emails per time of day"
						:datasets="mailsPerHour.datasets"
						:labels="mailsPerHour.labels"
					/>
				</div>
				<div class="column col-6 col-sm-12">
					<BarChart
						title="Weekdays"
						description="Number of emails per day of week"
						:datasets="mailsPerWeekday.datasets"
						:labels="mailsPerWeekday.labels"
					/>
				</div>
			</div>
			<!-- heat map for mail distribution over daytime on weekday -->
			<div class="columns mt-1-5">
				<div class="column col-6 col-sm-12 heatmap">
					<HeatMap
						title="Daytime Incoming"
						description="Number of incoming emails per weekday per hour"
						rgb="48, 206, 241"
						:dataset="stats.mailsPerWeekdayPerHour.in"
					/>
				</div>
				<div class="column col-6 col-sm-12 heatmap">
					<HeatMap
						title="Daytime Outgoing"
						description="Number of outgoing emails per weekday per hour"
						rgb="237, 47, 71"
						:dataset="stats.mailsPerWeekdayPerHour.out"
					/>
				</div>
			</div>
			<!-- footer -->
			<div class="columns mt-1-5">
				<div class="column col-12 text-gray text-center text-sm">
					<p>
						This data was retrieved on {{ figure.tstamp }}<br />
						Thunderbird Stats v{{ appVersion }} - star and fork this project on <a href="https://github.com/devmount/thunderbird-stats">Github</a>
					</p>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
// internal components
import LineChart from './components/LineChart.vue'
import BarChart from './components/BarChart.vue'
import HeatMap from './components/HeatMap.vue'

// chart data
import META from './data/meta.json'
import MAILS_PER_HOUR from './data/mails-per-hour.json'
import MAILS_PER_MONTH from './data/mails-per-month.json'
import MAILS_PER_YEAR from './data/mails-per-year.json'
import MAILS_PER_WEEKDAY from './data/mails-per-weekday.json'
import MAILS_PER_WEEKDAY_PER_HOUR from './data/mails-per-weekday-per-hour.json'

// initialize Chart.js with global configuration
import Chart from 'chart.js'
Chart.defaults.global.defaultFontColor = "#7e8d97"
Chart.defaults.global.elements.arc.borderWidth = 0
Chart.defaults.global.legend.display = false
Chart.defaults.global.tooltips.mode = 'index'
Chart.defaults.global.tooltips.intersect = false
Chart.defaults.global.tooltips.multiKeyBackground = '#000'
Chart.defaults.global.tooltips.titleMarginBottom = 10
Chart.defaults.global.tooltips.xPadding = 10
Chart.defaults.global.tooltips.yPadding = 10
Chart.defaults.global.tooltips.cornerRadius = 2
Chart.defaults.global.hover.mode = 'index'

export default {
	name: 'app',
	components: {
		LineChart,
		BarChart,
		HeatMap,
	},
	data () {
		return {
			view: 'total'
		}
	},
	computed: {
		appVersion() {
			return process.env.PACKAGE_VERSION;
		},
		addresses () {
			return Object.keys(META).reverse()
		},
		stats () {
			return {
				meta: META[this.view],
				mailsPerHour: MAILS_PER_HOUR[this.view],
				mailsPerMonth: MAILS_PER_MONTH[this.view],
				mailsPerYear: MAILS_PER_YEAR[this.view],
				mailsPerWeekday: MAILS_PER_WEEKDAY[this.view],
				mailsPerWeekdayPerHour: MAILS_PER_WEEKDAY_PER_HOUR[this.view],
			}
		},
		figure () {
			var meta = this.stats.meta
			var tstamp = new Date(meta.tstamp)
			return {
				in: meta.in.toLocaleString(),
				inPercentage: (meta.in/meta.total*100).toFixed(2),
				out: meta.out.toLocaleString(),
				outPercentage: (meta.out/meta.total*100).toFixed(2),
				total: meta.total.toLocaleString(),
				unread: meta.unread.toLocaleString(),
				unreadPercentage: (meta.unread/meta.total*100).toFixed(2),
				years: meta.years.toFixed(1),
				perday: (meta.total/meta.days.toFixed(1)).toFixed(2),
				perweek: (meta.total/meta.weeks.toFixed(1)).toFixed(1),
				permonth: (meta.total/meta.months.toFixed(1)).toFixed(1),
				peryear: (meta.total/meta.years.toFixed(1)).toFixed(1),
				oldest: new Date(meta.oldest),
				newest: new Date(meta.newest),
				tstamp: tstamp.toLocaleString(),
			}
		},
		mailsPerYear () {
			var din = this.stats.mailsPerYear.in
			var dout = this.stats.mailsPerYear.out
			var years = [], dsin = [], dsout = []
			for (let y = this.figure.oldest.getFullYear(); y <= this.figure.newest.getFullYear(); ++y) {
				years.push(y)
				dsin.push(din.hasOwnProperty(y) ? din[y] : 0)
				dsout.push(dout.hasOwnProperty(y) ? dout[y] : 0)
			}
			return {
				datasets: [
					{ label: 'Mails sent', data: dsout, color: 'rgb(237, 47, 71)', bcolor: 'rgb(237, 47, 71, .2)'  },
					{ label: 'Mails received', data: dsin,  color: 'rgb(48, 206, 242)', bcolor: 'rgb(48, 206, 242, .2)' },
				],
				labels: years
			}
		},
		mailsPerMonth () {
			var din = this.stats.mailsPerMonth.in
			var dout = this.stats.mailsPerMonth.out
			var months = [], dsin = [], dsout = [], skip = true
			var labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
			for (const year in din) {
				for (const month in din[year]) {
					// trim leading zero months
					if (din[year][month] == 0) {
						if (skip) continue
					} else {
						skip = false
					}
					// trim trailing zero months
					let d = new Date()
					if (d.getFullYear() < year || d.getFullYear() == year && d.getMonth()+1 < month) continue
					// push data
					months.push(year + ' ' + labels[month-1])
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
					{ label: 'Mails sent', data: dsout, color: 'rgb(237, 47, 71)', bcolor: 'rgb(237, 47, 71, .2)'  },
					{ label: 'Mails received', data: dsin,  color: 'rgb(48, 206, 242)', bcolor: 'rgb(48, 206, 242, .2)' },
				],
				labels: months
			}
		},
		mailsPerHour () {
			var din = this.stats.mailsPerHour.in
			var dout = this.stats.mailsPerHour.out
			var hours = [], dsin = [], dsout = []
			for (const hour in din) {
				hours.push(hour)
				dsin.push(din[hour])
				dsout.push(dout[hour])
			}
			return {
				datasets: [
					{ label: 'Mails sent', data: dsout, color: 'rgb(237, 47, 71)', bcolor: 'rgb(237, 47, 71, .2)'  },
					{ label: 'Mails received', data: dsin,  color: 'rgb(48, 206, 242)', bcolor: 'rgb(48, 206, 242, .2)' },
				],
				labels: hours
			}
		},
		mailsPerWeekday () {
			var din = this.stats.mailsPerWeekday.in
			var dout = this.stats.mailsPerWeekday.out
			var weekdays = [], dsin = [], dsout = []
			var days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
			for (const weekday in din) {
				weekdays.push(days[weekday])
				dsin.push(din[weekday])
				dsout.push(dout[weekday])
			}
			return {
				datasets: [
					{ label: 'Mails sent', data: dsout, color: 'rgb(237, 47, 71)', bcolor: 'rgb(237, 47, 71, .2)'  },
					{ label: 'Mails received', data: dsin,  color: 'rgb(48, 206, 242)', bcolor: 'rgb(48, 206, 242, .2)' },
				],
				labels: weekdays
			}
		},
	},
}
</script>

<style lang="scss">
// spectre config
$primary-color: #30cef1;
$secondary-color: #ed2f47;
$body-font-color: #cedae2;
$bg-color: #0d1219;
$bg-color-dark: #222627;
$bg-color-light: #0d1219;
$border-color: #222627;
$dark-color: #222627;
$gray-color: #7e8d97;
@import "node_modules/spectre.css/src/spectre";

// import fonts
@import url('https://fonts.googleapis.com/css?family=Fira+Mono');
</style>

<style lang="stylus">
font-mono = 'Fira Mono', 'Courier New', Courier, monospace

#app
	-webkit-font-smoothing antialiased
	-moz-osx-font-smoothing grayscale

h1, h2, h3
	text-align center
	font-weight 100

.figure
	font-size 2.75em;
	line-height 1em;
	font-weight 500;

.text-sm
	font-size .75em
.text-xs
	font-size .7em
.text-mono
	font-family font-mono

.mt-1
	margin-top 1rem
.mt-1-5
	margin-top 1.5rem

.chart
	h3
		margin-bottom .25em
	p
		margin 0

.tooltip
	position relative
	&::after
		background rgba(0, 0, 0, .8)
</style>
