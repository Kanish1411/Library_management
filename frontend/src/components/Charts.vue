<template>
    <div class="section-charts">
      <h2>Section Data Comparison</h2>
      <div>
        <h3>Reads Comparison Across Sections</h3>
        <canvas id="reads-chart"></canvas>
      </div>
      <div>
        <h3>PDFs Comparison Across Sections</h3>
        <canvas id="pdfs-chart"></canvas>
      </div>
      <div>
        <h3>Lends Comparison Across Sections</h3>
        <canvas id="lends-chart"></canvas>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { Chart, PieController, ArcElement, Tooltip, Legend } from 'chart.js';
  Chart.register(PieController, ArcElement, Tooltip, Legend);
  export default {
    data() {
      return {
        sec: [],
        reads: null,
        pdfs: null,
        lendsChart: null,
      };
    },
    methods: {
      fetchSectionData() {
        axios.get('/reads')
          .then(response => {
            this.sec = response.data;
            this.createCharts();
          })
          .catch(error => {
            console.log(error);
          });
      },
      createCharts() {
        const labels = this.sec.map(sec => `Section ${sec.sec_id}`);
        const readsData = this.sec.map(sec => sec.reads);
        const pdfsData = this.sec.map(sec => sec.pdfs);
        const lendsData = this.sec.map(sec => sec.lends);
  
        if (this.reads) this.reads.destroy();
        if (this.pdfs) this.pdfs.destroy();
        if (this.lendsChart) this.lendsChart.destroy();
  
        // Chart for Reads
        this.reads = new Chart(document.getElementById('reads-chart'), {
          type: 'pie',
          data: {
            labels: labels,
            datasets: [{
              label: 'Reads',
              backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe', '#ffce56', '#ffa500'],
              data: readsData
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: true
          }
        });
  
        // Chart for PDFs
        this.pdfs = new Chart(document.getElementById('pdfs-chart'), {
          type: 'pie',
          data: {
            labels: labels,
            datasets: [{
              label: 'PDFs',
              backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe', '#ffce56', '#ffa500'],
              data: pdfsData
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: true
          }
        });
  
        // Chart for Lends
        this.lendsChart = new Chart(document.getElementById('lends-chart'), {
          type: 'pie',
          data: {
            labels: labels,
            datasets: [{
              label: 'Lends',
              backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe', '#ffce56', '#ffa500'],
              data: lendsData
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: true
          }
        });
      }
    },
    mounted() {
      this.fetchSectionData();
    }
  };
  </script>
  
  <style scoped>
  .section-charts {
    width: 40%;
    margin: 0 auto;
  }
  
  canvas {
    width: 200px;
    height: 200px;
  }
  </style>
  