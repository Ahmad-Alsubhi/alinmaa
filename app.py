import dash
from dash import html, dash_table, dcc
import pandas as pd
import glob
import os

csv_dir = './'
dataframes = {}

for csv_file in glob.glob(os.path.join(csv_dir, '*.csv')):
    var_name = os.path.splitext(os.path.basename(csv_file))[0]
    try:
        df = pd.read_csv(csv_file)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        dataframes[var_name] = df
        print(f"تم تحميل {var_name} بنجاح!")
    except Exception as e:
        print(f"خطأ في تحميل {var_name}: {str(e)}")

app = dash.Dash(__name__)

styles = {
    'header': {
        'backgroundColor': '#2c3e50',
        'color': 'white',
        'padding': '20px',
        'textAlign': 'center',
        'borderRadius': '10px',
        'marginBottom': '20px'
    },
    'table-container': {
        'margin': '20px',
        'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
        'borderRadius': '1px',
        'overflow': 'hidden'
    },
    'table-header': {
        'backgroundColor': '#3498db',
        'color': 'white',
        'fontWeight': 'bold',
        'textAlign': 'center'
    },
    'table-cell': {
        'textAlign': 'right',
        'padding': '12px',
        'borderBottom': '1px solid #000000'
        
    },
    'tabs': {
        'margin': '20px'
    },
    'tab': {
        'backgroundColor': '#f8f9fa',
        'color': '#2c3e50',
        'padding': '10px',
        'border': '1px solid #ddd',
        'borderBottom': 'none',
        'borderRadius': '500px 500px 0 0'
    },
    'tab-selected': {
        'backgroundColor': '#3498db',
        'color': 'white',
        'padding': '5px',
        'border': '1px solid #3498db',
        'borderBottom': 'none'
    }
}

tabs = []
tab_content = []

tab_labels = {
    'balance_sheet': 'الميزانية العمومية',
    'income_statement': 'قائمة الدخل',
    'cash_flow': 'قائمة التدفقات النقدية',
    'equity_statement': 'قائمة حقوق المساهمين',
    'comprehensive_income': 'قائمة الدخل الشامل',
    'consolidated': 'البيانات المجمعة',
    'notes': 'الإيضاحات'
}

for i, (file_name, df) in enumerate(dataframes.items(), start=1):
    tab_label = tab_labels.get(file_name, file_name)
    tabs.append(
        dcc.Tab(
            label=tab_label,
            value=f'tab-{i}',
            style=styles['tab'],
            selected_style=styles['tab-selected']
        )
    )

app.layout = html.Div([
    html.Div([
        html.H1("البيانات المالية للبنك", style=styles['header']),
        
        dcc.Tabs(
            id="financial-tabs",
            value='tab-1',
            children=tabs,
            style=styles['tabs']
        ),
        
        html.Div(id='tabs-content')
    ])
])

@app.callback(
    dash.dependencies.Output('tabs-content', 'children'),
    [dash.dependencies.Input('financial-tabs', 'value')]
)
def render_content(tab):
    tab_index = int(tab.split('-')[1]) - 1
    file_name = list(dataframes.keys())[tab_index]
    df = dataframes[file_name]
    tab_label = tab_labels.get(file_name, file_name)
    return create_table(df, tab_label)

# دالة مساعدة لإنشاء الجداول بتنسيق جميل
def create_table(df, title):
    if df.empty:
        return html.Div("لا توجد بيانات متاحة", style={'textAlign': 'center', 'padding': '20px'})
    
    return html.Div([
        html.H3(title, style={'textAlign': 'center', 'color': '#2c3e50', 'marginTop': '20px'}),
        dash_table.DataTable(
            id=f'table-{title}',
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict('records'),
            style_table={
                'overflowX': 'auto',
                'borderRadius': '10px',
                'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.1)',
                'margin': '20px'
            },
            style_header=styles['table-header'],
            style_cell=styles['table-cell'],
            page_size=10,
            filter_action='native',
            sort_action='native'
        )
    ], style=styles['table-container'])

if __name__ == '__main__':
    app.run(debug=True)