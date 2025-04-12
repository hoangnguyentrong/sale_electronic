/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState, onWillStart, useRef, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets"


export class ChartRenderer extends Component {
    setup() {
        this.chartRef = useRef("chart")
        onWillStart(async ()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js")
        })

        onMounted(()=>this.renderChart());
    }

    renderChart(){
    console.log("Chart type:", this.props.type);
        new Chart(
        this.chartRef.el,
        {
                  type: this.props.type,
                  data: this.props.config?.data,
                  options: {
                    responsive: true,
                    plugins: {
                      legend: {
                        position: 'bottom',
                      },
                      title: {
                        display: true,
                        text: this.props.title,
                        position: 'bottom',
                      }
                    },
                    scales: this.props.config?.scales ?? {}
//                    scales: 'scales' in this.props.config ? this.props.config.scales : {}
                  },
        }
        );
    }

}

ChartRenderer.template = 'dashboard.ChartRenderer'