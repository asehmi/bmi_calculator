import streamlit as st

outside_display_area = st.container()

with st.expander('Show the code', expanded=True):
    with st.echo():
        state = st.session_state
        if 'WEIGHT' not in state:
            state.WEIGHT = 52.0
        if 'HEIGHT' not in state:
            state.HEIGHT = 1.54

        def _set_values_cb():
            state.WEIGHT = state['weight']
            state.HEIGHT = state['height']

        with outside_display_area:
            c1, c2 = st.columns([1,1])
            with c1:
                guage = st.empty()
            with c2:
                state.WEIGHT = st.number_input('Enter weight (kg)', min_value=50.0, max_value=150.0, value=state.WEIGHT, step=0.5, on_change=_set_values_cb, key='weight')
                state.HEIGHT = st.number_input('Enter height (m)', min_value=1.0, max_value=2.5, value=state.HEIGHT, step=0.1, on_change=_set_values_cb, key='height')

        BMI = round(state.WEIGHT/(state.HEIGHT**2), 1)

        bmi_thresholds = [13, 18.5, 25, 30, 43]
        level_labels = ['Severe Underweight', 'Underweight','Normal','Overweight','Obesity', 'Severe Obesity']

        if BMI <= bmi_thresholds[0]:
            level = level_labels[0]
        elif BMI <= bmi_thresholds[1]:
            level = level_labels[1]
        elif BMI <= bmi_thresholds[2]:
            level = level_labels[2]
        elif BMI <= bmi_thresholds[3]:
            level = level_labels[3]
        elif BMI <= bmi_thresholds[4]:
            level = level_labels[4]
        else:
            level = level_labels[5]

        bmi_gauge_lower = 13 # 0 degrees
        bmi_gauge_upper = 43 # 180 degrees

        bmi_guage_range = (bmi_gauge_upper - bmi_gauge_lower)
        BMI_adjusted = BMI if (BMI >= bmi_gauge_lower and BMI <= bmi_gauge_upper) else (
            bmi_gauge_lower if BMI < bmi_gauge_lower else bmi_gauge_upper
        )
        dial_rotation = round(((BMI_adjusted - bmi_gauge_lower) / bmi_guage_range) * 180.0, 1)

        svg = f"""
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="300px" height="163px" viewBox="0 0 300 163">
        <g transform="translate(18,18)" style="font-family:arial,helvetica,sans-serif;font-size: 12px;">
            <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7"></polygon>
                </marker>
                <path id="curvetxt1" d="M-4 140 A140 140, 0, 0, 1, 284 140" style="fill: none;"></path>
                <path id="curvetxt2" d="M33 43.6 A140 140, 0, 0, 1, 280 140" style="fill: #none;"></path>
                <path id="curvetxt3" d="M95 3 A140 140, 0, 0, 1, 284 140" style="fill: #none;"></path>
                <path id="curvetxt4" d="M235.4 33 A140 140, 0, 0, 1, 284 140" style="fill: #none;"></path>
            </defs>
            <path d="M0 140 A140 140, 0, 0, 1, 280 140 L140 140 Z" fill="#bc2020"></path>
            <path d="M6.9 96.7 A140 140, 0, 0, 1, 280 140 L140 140 Z" fill="#d38888"></path>
            <path d="M12.1 83.1 A140 140, 0, 0, 1, 280 140 L140 140 Z" fill="#ffe400"></path>
            <path d="M22.6 63.8 A140 140, 0, 0, 1, 96.7 6.9 L140 140 Z" fill="#008137"></path>
            <path d="M96.7 6.9 A140 140, 0, 0, 1, 280 140 L140 140 Z" fill="#ffe400"></path>
            <path d="M169.1 3.1 A140 140, 0, 0, 1, 280 140 L140 140 Z" fill="#d38888"></path>
            <path d="M233.7 36 A140 140, 0, 0, 1, 280 140 L140 140 Z" fill="#bc2020"></path>
            <path d="M273.1 96.7 A140 140, 0, 0, 1, 280 140 L140 140 Z" fill="#8a0101"></path>
            <path d="M45 140 A90 90, 0, 0, 1, 230 140 Z" fill="#fff"></path>
            <circle cx="140" cy="140" r="5" fill="#666"></circle>

            <g style="paint-order: stroke;stroke: #fff;stroke-width: 2px;">
                <text x="25" y="111" transform="rotate(-72, 25, 111)">16</text>
                <text x="30" y="96" transform="rotate(-66, 30, 96)">17</text>
                <text x="35" y="83" transform="rotate(-57, 35, 83)">18.5</text>
                <text x="97" y="29" transform="rotate(-18, 97, 29)">25</text>
                <text x="157" y="20" transform="rotate(12, 157, 20)">30</text>
                <text x="214" y="45" transform="rotate(42, 214, 45)">35</text>
                <text x="252" y="95" transform="rotate(72, 252, 95)">40</text>
            </g>

            <g style="font-size: 14px;">
                <text><textPath xlink:href="#curvetxt1">Underweight</textPath></text>
                <text><textPath xlink:href="#curvetxt2">Normal</textPath></text>
                <text><textPath xlink:href="#curvetxt3">Overweight</textPath></text>
                <text><textPath xlink:href="#curvetxt4">Obesity</textPath></text>
            </g>
            
            <line x1="140" y1="140" x2="65" y2="140" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)">
                <animateTransform attributeName="transform" attributeType="XML" type="rotate" from="0 140 140" to="{dial_rotation} 140 140" dur="1s" fill="freeze" repeatCount="1"></animateTransform>
            </line>
            
            <text x="67" y="120" style="font-size: 30px;font-weight:bold;color:#000;">BMI = {BMI}</text>
        </g>
        </svg>
        """

        with outside_display_area:
            guage.markdown(svg.replace('\n',''), unsafe_allow_html=True)
            st.subheader(f'BMI level is {level} ({BMI})')
            # st.caption(f'Rotation: {dial_rotation} degrees')
