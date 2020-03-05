<template>
<div class="chart">
	<h3 v-if="title">{{ title }}</h3>
	<p v-if="description" class="text-gray text-center">{{ description }}</p>
	<canvas :id='id'></canvas>
</div>
</template>

<script>
/* eslint no-undef: 0 */
export default {
	props: {
		title: String,
		description: String,
		labels: Array,
		datasets: Array,
	},
	data () {
		return {
			id: Math.random().toString(36).substring(7),
			chart: null
		}
	},
	mounted () {
		if (this.title != '' && this.labels && this.datasets) {
			this.draw()
		}
	},
	computed: {
		currentData () {
			let datasets = []
			for (let i = 0; i < this.datasets.length; i++) {
				const dataset = this.datasets[i];
				datasets.push({
					label: dataset.label,
					data: dataset.data,
					borderColor: dataset.color,
					borderWidth: 2,
					lineTension: 0.15,
					pointRadius: 0,
					backgroundColor: dataset.bcolor,
				})
			}
			return datasets
		}
	},
	methods: {
		draw () {
			this.chart = new Chart(this.id, {
				type: 'line',
				data: {
					datasets: this.currentData,
					labels: this.labels,
				},
				options: {
					scales: {
						xAxes: [{
							stacked: false,
							gridLines: {
								display: false,
							},
							ticks: {
								maxRotation: 0,
								autoSkipPadding: 10
							}
						}],
						yAxes: [{
							display: false,
							stacked: false,
							gridLines: {
								display: false,
							}
						}]
					}
				}
			})
		}
	},
	watch: {
		datasets () {
			this.draw()
		}
	}
}
</script>
