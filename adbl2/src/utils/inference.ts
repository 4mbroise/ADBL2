function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export async function inferRelation(relation) {
  await sleep(500)
  if(relation === "support") {
    return {support:0.6, attack:0.4}
  } else {
    return {attack:0.6, support:0.4}
  }
}


export function inferenceResultToDataset(res) {

  const labels = ["None"]
  const datasets = []

  datasets.push({
    label: 'Attack',
    data: [res.attack * 100],
    borderColor: 'rgb(255, 99, 132)',
    backgroundColor: '#ff9380',
  })

  datasets.push({
    label: 'Support',
    data: [res.support * 100],
    borderColor: 'rgb(53, 162, 235)',
    backgroundColor: '#bfff80',
  })

  return {
    labels: labels,
    datasets: datasets
  }
}

export const barOptions =  {
  // maintainAspectRatio: false,
  indexAxis: 'y' as const,
  plugins: {
    title: {
      display: false,
    },
    tooltip: {
      callbacks: {
         title : () => null
      }
   }
  },
  responsive: true,
  scales: {
    x: {
      stacked: true,
    },
    y: {
      stacked: true,
      ticks: {
        display: false
      }
    },
  },
};