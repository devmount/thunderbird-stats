<template>
<div>
	<h3>{{ title }}</h3>
	<canvas :id='id'></canvas>
</div>
</template>

<script>
/* eslint no-undef: 0 */
export default {
	props: {
		title: String,
		labels: Array,
		datasets: Array,
	},
	data () {
		return {
			id: Math.random().toString(36).substring(7)
		}
	},
	mounted () {
		if (this.title != '' && this.labels && this.datasets) {
			let datasets = []
			for (let i = 0; i < this.datasets.length; i++) {
				const dataset = this.datasets[i];
				datasets.push({
					label: dataset.label,
					data: dataset.data,
					backgroundColor: dataset.bcolor,
					borderWidth: 2,
					borderColor: dataset.color,
				})
			}
			new Chart(this.id, {
				type: 'bar',
				data: {
					datasets: datasets,
					labels: this.labels,
				},
				options: {
					scales: {
						xAxes: [{
							barPercentage: 1,
							categoryPercentage: .6,
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
	}
}
</script>
