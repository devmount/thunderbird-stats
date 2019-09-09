<template>
<div>
	<h3 class="text-center">{{ title }}</h3>
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
					borderColor: dataset.color,
					borderWidth: 2,
					lineTension: 0.15,
					pointBorderColor: 'rgb(0, 0, 0, 0)',
					pointRadius: 0,
					backgroundColor: dataset.bcolor,
				})
			}
			new Chart(this.id, {
				type: 'line',
				data: {
					datasets: datasets,
					labels: this.labels,
				},
			})
		}
	}
}
</script>
