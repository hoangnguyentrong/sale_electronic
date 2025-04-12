/** @odoo-module **/
import { registry } from "@web/core/registry";
import { KpiCard } from "./kpi_card/kpi_card"
import { ChartRenderer } from "./chart_renderer/chart_renderer"
import { Component, useState, onWillStart, useRef, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets"
import { useService } from "@web/core/utils/hooks";
import { getColor } from "@web/views/calendar/colors";
import { nextTick } from "@odoo/owl";

export class OwlSalesDashboard extends Component {
    // top products
        async getTopProducts(){
        let domain = [['state', 'in', ['sale', 'done']]]
        if (this.state.period > 0){
            domain.push(['date','>', this.state.current_date])
        }

        const data = await this.orm.readGroup("sale.report", domain,
                     ['product_id', 'price_total'], ['product_id'],
                     { limit: 5, orderby: "price_total desc" })
        if(data.length > 0){
            this.state.topProducts = {
                 data: {
                    labels: data.map(d => d.product_id[1]),
                      datasets: [
                      {
                        label: 'Total',
                        data: data.map(d => d.price_total),
                        hoverOffset: 4,
                        backgroundColor: [
                            '#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#FFD700'
                        ],
                      },{
                        label: 'Count',
                        data: data.map(d => d.product_id_count),
                        hoverOffset: 4,
                        backgroundColor: [
                            '#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#FFD700'
                        ],
                    }]
                },

            }
        };
    }
    setup() {
        this.state = useState({
            quotations: {
                value:10,
                percentage:6,

            },
            topProducts: { data: { labels: [], datasets: [] } },
            period:90,
        })
        this.orm = useService("orm")
        this.model = "sale.order"
        this.actionService = useService("action");

        onWillStart(async ()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.4/moment.min.js");
            this.getDates()
            await this.getQuotations()
            await this.getOrders()

            //Chart
            await this.getTopProducts()
            })
    }

    async onchangePeriod(){
        this.getDates()
        await this.getQuotations()
        await this.getOrders()

        //Chart
        await this.getTopProducts()
    }
    getDates(){
        this.state.current_date = moment().subtract(this.state.period, 'days').format('L')
        this.state.previous_date = moment().subtract(this.state.period * 2, 'days').format('L')
    }
    async getQuotations(){
        let domain = [['state', 'in', ['sent', 'draft']]]
        if(this.state.period > 0){
            domain.push(['date_order', '>', this.state.current_date])
            }
        const data = await this.orm.searchCount(this.model, domain)
        this.state.quotations.value = data
        let prev_domain = [['state', 'in', ['sent', 'draft']]]
        if(this.state.period > 0){
            prev_domain.push(['date_order', '>', this.state.previous_date],['date_order', '<=', this.state.current_date])
            }
        const prev_data = await this.orm.searchCount(this.model, prev_domain)
        const percentage = ((data - prev_data)/prev_data) * 100
        this.state.quotations.percentage = percentage.toFixed(2)
        console.log(this.state.previous_date, this.state.current_date)
    }
    async getOrders(){
        let domain = [['state', 'in', ['sale', 'done']]]
        if(this.state.period > 0){
            domain.push(['date_order', '>', this.state.current_date])
            }
        const data = await this.orm.searchCount(this.model, domain)
       // this.state.quotations.value = data
        let prev_domain = [['state', 'in', ['sale', 'done']]]
        if(this.state.period > 0){
            prev_domain.push(['date_order', '>', this.state.previous_date],['date_order', '<=', this.state.current_date])
            }
        const prev_data = await this.orm.searchCount(this.model, prev_domain)
        const percentage = ((data - prev_data)/prev_data) * 100
        //this.state.quotations.percentage = percentage.toFixed(2)

        //revenues
        const current_revenue = await this.orm.readGroup(this.model, domain, ['amount_total:sum'], [])
        const prev_revenue = await this.orm.readGroup(this.model, prev_domain, ['amount_total:sum'], [])
        const revenue_percentage = ((current_revenue[0].amount_total - prev_revenue[0].amount_total)/ prev_revenue[0].amount_total) * 100
        console.log("Current revenue data:", current_revenue);
        console.log("Previous revenue data:", prev_revenue);
        //average
        const current_average = await this.orm.readGroup(this.model, domain, ['amount_total:avg'], [])
        const prev_average = await this.orm.readGroup(this.model, prev_domain, ['amount_total:avg'], [])
        const average_percentage = ((current_average[0].amount_total - prev_average[0].amount_total)/ prev_average[0].amount_total) * 100
        this.state.orders = {
            value: data,
            percentage: percentage.toFixed(2),
            revenue: `${(current_revenue[0].amount_total/1000).toFixed(2)}K`,
            revenue_percentage: revenue_percentage.toFixed(2),
            average: `${(current_average[0].amount_total/1000).toFixed(2)}K`,
            average_percentage: average_percentage.toFixed(2),
        }
    }
    viewQuotations(){
//        this.actionService.doAction("sale.action_quotations_with_onboarding", {
//            additionalContext: {
//                search_default_draft: 1,
//                search_default_my_quotation: 2,
//
//            }
//        })
        let domain = [['state', 'in', ['sent', 'draft']]];
        if(this.state.period > 0){
            domain.push(['date_order', '>', this.state.current_date]);
        }
        let list_view = this.orm.searchRead("ir.model.data", [['name', '=', 'view_quotation_tree_with_onboarding']], ['res_id'])
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Quotations",
            res_model: this.model,
            domain: domain,
            views: [
                [list_view.length > 0 ? list_view[0].res_id : false ,"list"],
                [false, "form"]
            ]
        });
    }
    viewOrders(){
        let prev_domain = [['state', 'in', ['sale', 'done']]]
        if(this.state.period > 0){
            prev_domain.push(['date_order', '>', this.state.previous_date],['date_order', '<=', this.state.current_date])
            }

        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Quotations",
            res_model: this.model,
            domain: prev_domain,
            context: {"group_by": "date_order"},
            views: [
                [false, "list"],
                [false, "form"]
            ]
        });
    }
}

OwlSalesDashboard.template = 'dashboard.OwlSalesDashboard'
OwlSalesDashboard.components = { KpiCard, ChartRenderer }

registry.category('actions').add('owl.sales_dashboard', OwlSalesDashboard);