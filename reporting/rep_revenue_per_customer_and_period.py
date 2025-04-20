create or replace table reporting_db.rep_revenue_per_customer_and_period as

 with payments as (
  select     
  p.payment_id,
    p.customer_id,
    p.staff_id,
    p.rental_id,
    p.payment_amount,
    p.payment_date
  from cosmic-strategy-454618-b0.staging_db.stg_payment p
  join cosmic-strategy-454618-b0.staging_db.stg_rental r
    on p.rental_id = r.rental_id
  join cosmic-strategy-454618-b0.staging_db.stg_inventory i
    on r.inventory_id = i.inventory_id
  join cosmic-strategy-454618-b0.staging_db.stg_film f
    on i.film_id = f.film_id
  where f.film_title != 'GOODFELLAS SALUTE'
),
 customers as (
 select *
 from cosmic-strategy-454618-b0.staging_db.stg_customer
 )
 , reporting_dates as (
 select *
 from cosmic-strategy-454618-b0.reporting_db.reporting_periods_table
 where reporting_period in ('Day','Month','Year')
 )
 , payments_per_period as (
 select
 'Day' as reporting_period
 , date_trunc(payments.payment_date, day) as reporting_date
 , customers.customer_id
 , sum(payment_amount) as total_revenue
from payments
 left join customers on payments.customer_id =
 customers.customer_id
 group by 1,2,3
 union all
 select
 'Month' as reporting_period
 , date_trunc(payments.payment_date, month) as reporting_date
 , customers.customer_id
 , sum(payment_amount) as total_revenue
 from payments
  left join customers on payments.customer_id =
 customers.customer_id
 group by 1,2,3
 union all
 select
 'Year' as reporting_period
 , date_trunc(payments.payment_date, year) as reporting_date
 , customers.customer_id
 , sum(payment_amount) as total_revenue
 from payments
  left join customers on payments.customer_id =
 customers.customer_id
 group by 1,2,3
 )

 , final as (
 select
 reporting_dates.reporting_period
 , reporting_dates.reporting_date
 , payments_per_period.customer_id
 , payments_per_period.total_revenue
 from reporting_dates
 inner join payments_per_period
 on reporting_dates.reporting_period =
 payments_per_period.reporting_period
 and reporting_dates.reporting_date =
 payments_per_period.reporting_date
 where reporting_dates.reporting_period = 'Day'
 union all
select
 reporting_dates.reporting_period
 , reporting_dates.reporting_date
 , payments_per_period.customer_id
 , payments_per_period.total_revenue
 from reporting_dates
 inner join payments_per_period
 on reporting_dates.reporting_period =
 payments_per_period.reporting_period
 and reporting_dates.reporting_date =
 payments_per_period.reporting_date
 where reporting_dates.reporting_period = 'Month'
 union all
 select
 reporting_dates.reporting_period
 , reporting_dates.reporting_date
 , payments_per_period.customer_id
 , payments_per_period.total_revenue
 from reporting_dates
 inner join payments_per_period
 on reporting_dates.reporting_period =
 payments_per_period.reporting_period
 and reporting_dates.reporting_date =
 payments_per_period.reporting_date
 where reporting_dates.reporting_period = 'Year'
 )
 select * from final 