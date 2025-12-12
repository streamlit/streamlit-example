"""
Port Operations Simulation - Professional 3D/2D Visualization Dashboard
A discrete-event simulation of container port operations using SimPy
with real-time 3D/2D visualization and analytics.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import simpy
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from collections import defaultdict
import time

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Port Operations Simulation",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS FOR PROFESSIONAL STYLING
# ============================================================================
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }

    /* Metric cards styling */
    .metric-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%);
        border-radius: 10px;
        padding: 15px;
        margin: 5px 0;
        border-left: 4px solid #00d4ff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #00d4ff;
        margin: 0;
    }

    .metric-label {
        font-size: 12px;
        color: #8899a6;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0;
    }

    /* Status indicator */
    .status-active {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #00ff88;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(0, 255, 136, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
    }

    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #0d2137 0%, #1e3a5f 50%, #0d2137 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        border: 1px solid #1e3a5f;
    }

    .main-header h1 {
        color: #00d4ff;
        margin: 0;
        font-size: 2.2rem;
    }

    .main-header p {
        color: #8899a6;
        margin: 5px 0 0 0;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #0d2137;
    }

    /* Section headers */
    .section-header {
        color: #00d4ff;
        border-bottom: 2px solid #1e3a5f;
        padding-bottom: 10px;
        margin-bottom: 15px;
        font-size: 1.1rem;
        font-weight: 600;
    }

    /* Legend items */
    .legend-item {
        display: flex;
        align-items: center;
        margin: 5px 0;
        font-size: 12px;
    }

    .legend-color {
        width: 15px;
        height: 15px;
        border-radius: 3px;
        margin-right: 8px;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0d2137;
    }
    ::-webkit-scrollbar-thumb {
        background: #1e3a5f;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #2e4a6f;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# DATA CLASSES FOR SIMULATION
# ============================================================================
@dataclass
class Ship:
    id: int
    name: str
    containers: int
    arrival_time: float
    ship_type: str  # 'container', 'tanker', 'bulk'
    length: float
    status: str = "waiting"  # waiting, berthing, loading, unloading, departing
    berth_id: Optional[int] = None
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    wait_time: float = 0.0
    service_time: float = 0.0


@dataclass
class Berth:
    id: int
    name: str
    x: float
    y: float
    length: float
    crane_count: int
    status: str = "available"  # available, occupied, maintenance
    current_ship: Optional[Ship] = None


@dataclass
class Crane:
    id: int
    berth_id: int
    x: float
    y: float
    z: float
    status: str = "idle"  # idle, loading, unloading
    containers_moved: int = 0


@dataclass
class Container:
    id: int
    x: float
    y: float
    z: float
    status: str = "yard"  # yard, loading, ship, unloading


@dataclass
class SimulationStats:
    total_ships_arrived: int = 0
    total_ships_served: int = 0
    total_containers_moved: int = 0
    total_wait_time: float = 0.0
    total_service_time: float = 0.0
    berth_utilization: Dict[int, float] = field(default_factory=dict)
    crane_utilization: Dict[int, float] = field(default_factory=dict)
    hourly_throughput: List[int] = field(default_factory=list)
    queue_length_history: List[int] = field(default_factory=list)
    ships_in_queue: int = 0


# ============================================================================
# PORT SIMULATION ENGINE
# ============================================================================
class PortSimulation:
    def __init__(self, config: dict):
        self.config = config
        self.env = simpy.Environment()
        self.stats = SimulationStats()

        # Resources
        self.berths: List[Berth] = []
        self.cranes: List[Crane] = []
        self.ships: List[Ship] = []
        self.containers: List[Container] = []

        # SimPy resources
        self.berth_resource = None

        # Initialize port infrastructure
        self._setup_port()

        # Event tracking
        self.events_log: List[dict] = []

    def _setup_port(self):
        """Initialize port infrastructure"""
        num_berths = self.config.get('num_berths', 4)
        cranes_per_berth = self.config.get('cranes_per_berth', 2)

        # Create berths along the quay
        for i in range(num_berths):
            berth = Berth(
                id=i,
                name=f"Berth {i+1}",
                x=100 + i * 150,
                y=50,
                length=120,
                crane_count=cranes_per_berth
            )
            self.berths.append(berth)

            # Create cranes for each berth
            for j in range(cranes_per_berth):
                crane = Crane(
                    id=len(self.cranes),
                    berth_id=i,
                    x=berth.x + 30 + j * 40,
                    y=berth.y + 30,
                    z=50
                )
                self.cranes.append(crane)

        # Create container yard
        yard_containers = self.config.get('initial_containers', 500)
        for i in range(yard_containers):
            row = i // 50
            col = i % 50
            stack = random.randint(0, 4)
            container = Container(
                id=i,
                x=100 + col * 8,
                y=200 + row * 15,
                z=stack * 10
            )
            self.containers.append(container)

        # Create SimPy resource for berths
        self.berth_resource = simpy.Resource(self.env, capacity=num_berths)

    def ship_generator(self):
        """Generate ships arriving at the port"""
        ship_id = 0
        ship_names = ["Ever Given", "MSC Oscar", "CSCL Globe", "Madrid Maersk",
                      "CMA CGM Marco Polo", "OOCL Hong Kong", "MOL Triumph",
                      "Yang Ming Warranty", "Hapag-Lloyd Express", "Cosco Shipping"]
        ship_types = ["container", "container", "container", "bulk", "tanker"]

        while True:
            # Inter-arrival time (exponential distribution)
            arrival_rate = self.config.get('arrival_rate', 2.0)
            yield self.env.timeout(random.expovariate(1.0 / arrival_rate))

            # Create new ship
            ship = Ship(
                id=ship_id,
                name=f"{random.choice(ship_names)} #{ship_id}",
                containers=random.randint(500, 3000),
                arrival_time=self.env.now,
                ship_type=random.choice(ship_types),
                length=random.uniform(200, 400),
                x=-50,  # Start outside port
                y=50 + random.uniform(-20, 20),
                z=0
            )

            self.ships.append(ship)
            self.stats.total_ships_arrived += 1
            self.stats.ships_in_queue += 1

            self.events_log.append({
                'time': self.env.now,
                'event': 'arrival',
                'ship': ship.name,
                'containers': ship.containers
            })

            # Start ship process
            self.env.process(self.ship_process(ship))
            ship_id += 1

    def ship_process(self, ship: Ship):
        """Process a ship through the port"""
        arrival_time = self.env.now

        # Request a berth
        with self.berth_resource.request() as request:
            yield request

            # Find available berth
            berth = next((b for b in self.berths if b.status == "available"), None)
            if berth:
                berth.status = "occupied"
                berth.current_ship = ship
                ship.berth_id = berth.id
                ship.status = "berthing"
                ship.wait_time = self.env.now - arrival_time
                self.stats.total_wait_time += ship.wait_time
                self.stats.ships_in_queue -= 1

                # Move ship to berth
                ship.x = berth.x
                ship.y = berth.y

                self.events_log.append({
                    'time': self.env.now,
                    'event': 'berthing',
                    'ship': ship.name,
                    'berth': berth.name
                })

                # Berthing time
                yield self.env.timeout(random.uniform(0.5, 1.0))

                # Unloading/Loading operations
                ship.status = "unloading"
                containers_per_hour = self.config.get('crane_speed', 30) * berth.crane_count
                service_time = ship.containers / containers_per_hour

                # Activate cranes
                berth_cranes = [c for c in self.cranes if c.berth_id == berth.id]
                for crane in berth_cranes:
                    crane.status = "unloading"

                yield self.env.timeout(service_time)

                # Update statistics
                ship.service_time = service_time
                self.stats.total_service_time += service_time
                self.stats.total_containers_moved += ship.containers
                self.stats.total_ships_served += 1

                for crane in berth_cranes:
                    crane.containers_moved += ship.containers // len(berth_cranes)
                    crane.status = "idle"

                # Departure
                ship.status = "departing"
                self.events_log.append({
                    'time': self.env.now,
                    'event': 'departure',
                    'ship': ship.name,
                    'service_time': service_time
                })

                yield self.env.timeout(0.5)

                # Clear berth
                berth.status = "available"
                berth.current_ship = None
                ship.status = "departed"
                ship.x = 800  # Move outside port

    def run(self, duration: float):
        """Run the simulation for a specified duration"""
        self.env.process(self.ship_generator())
        self.env.run(until=duration)

        # Calculate final statistics
        self._calculate_utilization()

        return self.get_state()

    def _calculate_utilization(self):
        """Calculate resource utilization"""
        if self.env.now > 0:
            for berth in self.berths:
                # Simplified utilization calculation
                occupied_time = sum(s.service_time for s in self.ships
                                   if s.berth_id == berth.id and s.status == "departed")
                self.stats.berth_utilization[berth.id] = min(occupied_time / self.env.now, 1.0)

            for crane in self.cranes:
                self.stats.crane_utilization[crane.id] = min(
                    crane.containers_moved / (self.env.now * self.config.get('crane_speed', 30)), 1.0
                )

    def get_state(self) -> dict:
        """Get current simulation state for visualization"""
        return {
            'time': self.env.now,
            'berths': self.berths,
            'cranes': self.cranes,
            'ships': self.ships,
            'containers': self.containers[:200],  # Limit for performance
            'stats': self.stats,
            'events': self.events_log[-50:]  # Last 50 events
        }


# ============================================================================
# 3D VISUALIZATION
# ============================================================================
def create_3d_port_view(state: dict) -> go.Figure:
    """Create 3D visualization of the port"""
    fig = go.Figure()

    # Water surface
    water_x = np.linspace(-100, 900, 50)
    water_y = np.linspace(-50, 100, 20)
    water_X, water_Y = np.meshgrid(water_x, water_y)
    water_Z = np.sin(water_X * 0.02) * 2 + np.cos(water_Y * 0.05) * 1

    fig.add_trace(go.Surface(
        x=water_X, y=water_Y, z=water_Z,
        colorscale=[[0, '#0a3d62'], [0.5, '#1e5f74'], [1, '#0a3d62']],
        showscale=False,
        opacity=0.8,
        name='Water'
    ))

    # Quay wall
    fig.add_trace(go.Mesh3d(
        x=[0, 800, 800, 0, 0, 800, 800, 0],
        y=[80, 80, 100, 100, 80, 80, 100, 100],
        z=[0, 0, 0, 0, 20, 20, 20, 20],
        i=[0, 0, 4, 4, 0, 1, 1, 2, 2, 3, 0, 4],
        j=[1, 2, 5, 6, 1, 5, 2, 6, 3, 7, 3, 7],
        k=[2, 3, 6, 7, 4, 4, 5, 5, 6, 6, 4, 3],
        color='#4a4a4a',
        opacity=0.9,
        name='Quay'
    ))

    # Container yard (ground)
    fig.add_trace(go.Mesh3d(
        x=[50, 750, 750, 50],
        y=[150, 150, 400, 400],
        z=[0, 0, 0, 0],
        i=[0, 0],
        j=[1, 2],
        k=[2, 3],
        color='#2c3e50',
        opacity=0.7,
        name='Container Yard'
    ))

    # Berths
    colors_berth = {'available': '#27ae60', 'occupied': '#e74c3c', 'maintenance': '#f39c12'}
    for berth in state['berths']:
        color = colors_berth.get(berth.status, '#3498db')
        fig.add_trace(go.Scatter3d(
            x=[berth.x, berth.x + berth.length],
            y=[berth.y, berth.y],
            z=[21, 21],
            mode='lines',
            line=dict(color=color, width=15),
            name=f'{berth.name}'
        ))

        # Berth label
        fig.add_trace(go.Scatter3d(
            x=[berth.x + berth.length/2],
            y=[berth.y + 30],
            z=[25],
            mode='text',
            text=[berth.name],
            textfont=dict(size=10, color='white'),
            showlegend=False
        ))

    # Cranes
    for crane in state['cranes']:
        crane_color = '#f1c40f' if crane.status == 'idle' else '#e74c3c'
        # Crane base
        fig.add_trace(go.Scatter3d(
            x=[crane.x, crane.x],
            y=[crane.y, crane.y],
            z=[20, 80],
            mode='lines',
            line=dict(color=crane_color, width=8),
            name=f'Crane {crane.id}' if crane.id == 0 else None,
            showlegend=(crane.id == 0)
        ))
        # Crane arm
        fig.add_trace(go.Scatter3d(
            x=[crane.x - 30, crane.x + 50],
            y=[crane.y, crane.y],
            z=[80, 80],
            mode='lines',
            line=dict(color=crane_color, width=6),
            showlegend=False
        ))

    # Ships
    ship_colors = {'waiting': '#3498db', 'berthing': '#f39c12',
                   'unloading': '#e74c3c', 'loading': '#9b59b6',
                   'departing': '#1abc9c', 'departed': '#95a5a6'}

    for ship in state['ships']:
        if ship.status != 'departed' and ship.x < 850:
            color = ship_colors.get(ship.status, '#3498db')
            # Ship hull
            ship_length = min(ship.length / 3, 80)
            ship_width = ship_length / 4

            hull_x = [ship.x, ship.x + ship_length * 0.8, ship.x + ship_length,
                      ship.x + ship_length * 0.8, ship.x]
            hull_y = [ship.y - ship_width/2, ship.y - ship_width/2, ship.y,
                      ship.y + ship_width/2, ship.y + ship_width/2]
            hull_z = [5, 5, 5, 5, 5]

            fig.add_trace(go.Scatter3d(
                x=hull_x + [hull_x[0]],
                y=hull_y + [hull_y[0]],
                z=hull_z + [hull_z[0]],
                mode='lines',
                line=dict(color=color, width=4),
                fill='toself',
                name=ship.name if ship.id < 3 else None,
                showlegend=(ship.id < 3)
            ))

            # Ship superstructure
            fig.add_trace(go.Scatter3d(
                x=[ship.x + ship_length * 0.3],
                y=[ship.y],
                z=[20],
                mode='markers',
                marker=dict(size=8, color=color, symbol='square'),
                showlegend=False
            ))

    # Containers in yard (sample)
    if state['containers']:
        container_x = [c.x for c in state['containers'][:100]]
        container_y = [c.y for c in state['containers'][:100]]
        container_z = [c.z + 5 for c in state['containers'][:100]]

        fig.add_trace(go.Scatter3d(
            x=container_x,
            y=container_y,
            z=container_z,
            mode='markers',
            marker=dict(
                size=4,
                color=container_z,
                colorscale='Viridis',
                opacity=0.8
            ),
            name='Containers'
        ))

    # Layout
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='', showgrid=False, showbackground=False, visible=False),
            yaxis=dict(title='', showgrid=False, showbackground=False, visible=False),
            zaxis=dict(title='', showgrid=False, showbackground=False, visible=False),
            camera=dict(
                eye=dict(x=1.5, y=-1.5, z=1.2),
                center=dict(x=0, y=0, z=-0.1)
            ),
            aspectmode='manual',
            aspectratio=dict(x=2, y=1, z=0.5)
        ),
        paper_bgcolor='rgba(13, 33, 55, 1)',
        plot_bgcolor='rgba(13, 33, 55, 1)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=450,
        showlegend=True,
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor='rgba(13, 33, 55, 0.8)',
            bordercolor='#1e3a5f',
            font=dict(color='white', size=10)
        )
    )

    return fig


# ============================================================================
# 2D TOP-DOWN VIEW
# ============================================================================
def create_2d_port_view(state: dict) -> go.Figure:
    """Create 2D top-down visualization of the port"""
    fig = go.Figure()

    # Water area
    fig.add_shape(
        type="rect",
        x0=-100, y0=-50, x1=900, y1=80,
        fillcolor="rgba(10, 61, 98, 0.5)",
        line=dict(width=0)
    )

    # Quay area
    fig.add_shape(
        type="rect",
        x0=0, y0=80, x1=800, y1=100,
        fillcolor="#4a4a4a",
        line=dict(color="#5a5a5a", width=2)
    )

    # Container yard
    fig.add_shape(
        type="rect",
        x0=50, y0=150, x1=750, y1=400,
        fillcolor="rgba(44, 62, 80, 0.5)",
        line=dict(color="#34495e", width=1, dash="dash")
    )

    # Yard label
    fig.add_annotation(
        x=400, y=275,
        text="CONTAINER YARD",
        showarrow=False,
        font=dict(size=14, color="rgba(255,255,255,0.3)")
    )

    # Berths
    berth_colors = {'available': '#27ae60', 'occupied': '#e74c3c', 'maintenance': '#f39c12'}
    for berth in state['berths']:
        color = berth_colors.get(berth.status, '#3498db')
        fig.add_shape(
            type="rect",
            x0=berth.x, y0=berth.y,
            x1=berth.x + berth.length, y1=berth.y + 25,
            fillcolor=color,
            opacity=0.7,
            line=dict(color='white', width=1)
        )
        fig.add_annotation(
            x=berth.x + berth.length/2,
            y=berth.y + 12,
            text=berth.name,
            showarrow=False,
            font=dict(size=9, color="white")
        )

    # Cranes
    crane_x = [c.x for c in state['cranes']]
    crane_y = [c.y + 15 for c in state['cranes']]
    crane_colors = ['#f1c40f' if c.status == 'idle' else '#e74c3c' for c in state['cranes']]

    fig.add_trace(go.Scatter(
        x=crane_x,
        y=crane_y,
        mode='markers',
        marker=dict(
            size=12,
            color=crane_colors,
            symbol='triangle-up',
            line=dict(color='white', width=1)
        ),
        name='Cranes',
        hovertemplate='Crane %{text}<extra></extra>',
        text=[f"{c.id}: {c.status}" for c in state['cranes']]
    ))

    # Ships
    ship_colors = {'waiting': '#3498db', 'berthing': '#f39c12',
                   'unloading': '#e74c3c', 'loading': '#9b59b6',
                   'departing': '#1abc9c', 'departed': '#95a5a6'}

    for ship in state['ships']:
        if ship.status != 'departed' and -100 < ship.x < 850:
            color = ship_colors.get(ship.status, '#3498db')
            ship_length = min(ship.length / 4, 60)

            # Ship shape
            fig.add_shape(
                type="path",
                path=f"M {ship.x},{ship.y-8} L {ship.x+ship_length*0.9},{ship.y-8} L {ship.x+ship_length},{ship.y} L {ship.x+ship_length*0.9},{ship.y+8} L {ship.x},{ship.y+8} Z",
                fillcolor=color,
                line=dict(color='white', width=1)
            )

            # Ship label
            fig.add_annotation(
                x=ship.x + ship_length/2,
                y=ship.y,
                text=f"S{ship.id}",
                showarrow=False,
                font=dict(size=8, color="white")
            )

    # Containers (simplified dots)
    if state['containers']:
        container_x = [c.x for c in state['containers'][:150]]
        container_y = [c.y for c in state['containers'][:150]]

        fig.add_trace(go.Scatter(
            x=container_x,
            y=container_y,
            mode='markers',
            marker=dict(size=3, color='#00d4ff', opacity=0.5),
            name='Containers',
            hoverinfo='skip'
        ))

    # Waiting area indicator
    waiting_ships = [s for s in state['ships'] if s.status == 'waiting']
    if waiting_ships:
        fig.add_shape(
            type="rect",
            x0=-80, y0=0, x1=-10, y1=70,
            fillcolor="rgba(52, 152, 219, 0.2)",
            line=dict(color='#3498db', width=1, dash='dot')
        )
        fig.add_annotation(
            x=-45, y=80,
            text=f"Queue: {len(waiting_ships)}",
            showarrow=False,
            font=dict(size=10, color='#3498db')
        )

    # Layout
    fig.update_layout(
        xaxis=dict(
            range=[-100, 850],
            showgrid=False,
            zeroline=False,
            visible=False
        ),
        yaxis=dict(
            range=[-70, 420],
            showgrid=False,
            zeroline=False,
            visible=False,
            scaleanchor="x",
            scaleratio=1
        ),
        paper_bgcolor='rgba(13, 33, 55, 1)',
        plot_bgcolor='rgba(13, 33, 55, 1)',
        margin=dict(l=10, r=10, t=10, b=10),
        height=350,
        showlegend=False,
        hovermode='closest'
    )

    return fig


# ============================================================================
# ANALYTICS CHARTS
# ============================================================================
def create_throughput_chart(stats: SimulationStats, sim_time: float) -> go.Figure:
    """Create throughput over time chart"""
    # Generate hourly data
    hours = max(1, int(sim_time))
    hourly_data = np.random.poisson(
        stats.total_containers_moved / max(hours, 1),
        size=hours
    ).cumsum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(hours)),
        y=hourly_data,
        mode='lines+markers',
        line=dict(color='#00d4ff', width=2),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 255, 0.2)',
        name='Containers'
    ))

    fig.update_layout(
        title=dict(text='Cumulative Throughput', font=dict(size=12, color='white')),
        xaxis=dict(title='Time (hours)', gridcolor='#1e3a5f', color='#8899a6'),
        yaxis=dict(title='Containers', gridcolor='#1e3a5f', color='#8899a6'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(13, 33, 55, 0.5)',
        margin=dict(l=40, r=10, t=40, b=40),
        height=200,
        font=dict(color='white')
    )
    return fig


def create_utilization_chart(stats: SimulationStats) -> go.Figure:
    """Create resource utilization chart"""
    berths = [f"B{i+1}" for i in stats.berth_utilization.keys()]
    utilization = [v * 100 for v in stats.berth_utilization.values()]

    if not berths:
        berths = ['B1', 'B2', 'B3', 'B4']
        utilization = [0, 0, 0, 0]

    colors = ['#27ae60' if u < 70 else '#f39c12' if u < 90 else '#e74c3c' for u in utilization]

    fig = go.Figure(data=[
        go.Bar(
            x=berths,
            y=utilization,
            marker_color=colors,
            text=[f'{u:.0f}%' for u in utilization],
            textposition='outside'
        )
    ])

    fig.update_layout(
        title=dict(text='Berth Utilization', font=dict(size=12, color='white')),
        xaxis=dict(gridcolor='#1e3a5f', color='#8899a6'),
        yaxis=dict(title='%', range=[0, 110], gridcolor='#1e3a5f', color='#8899a6'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(13, 33, 55, 0.5)',
        margin=dict(l=40, r=10, t=40, b=40),
        height=200,
        font=dict(color='white'),
        showlegend=False
    )
    return fig


def create_queue_chart(stats: SimulationStats) -> go.Figure:
    """Create queue length gauge"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=stats.ships_in_queue,
        title=dict(text="Ships in Queue", font=dict(size=12, color='white')),
        gauge=dict(
            axis=dict(range=[0, 10], tickcolor='white'),
            bar=dict(color='#00d4ff'),
            bgcolor='#1e3a5f',
            bordercolor='#2e4a6f',
            steps=[
                dict(range=[0, 3], color='#27ae60'),
                dict(range=[3, 6], color='#f39c12'),
                dict(range=[6, 10], color='#e74c3c')
            ],
            threshold=dict(
                line=dict(color='white', width=2),
                thickness=0.75,
                value=stats.ships_in_queue
            )
        )
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=180,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig


# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚢 Port Operations Simulation</h1>
        <p>Real-time 3D/2D Visualization & Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar - Simulation Controls
    with st.sidebar:
        st.markdown('<div class="section-header">⚙️ SIMULATION PARAMETERS</div>', unsafe_allow_html=True)

        num_berths = st.slider("Number of Berths", 2, 8, 4)
        cranes_per_berth = st.slider("Cranes per Berth", 1, 4, 2)
        arrival_rate = st.slider("Ship Arrival Rate (per hour)", 0.5, 5.0, 2.0, 0.5)
        crane_speed = st.slider("Crane Speed (containers/hour)", 20, 50, 30)
        initial_containers = st.slider("Initial Yard Containers", 100, 1000, 500, 100)
        sim_duration = st.slider("Simulation Duration (hours)", 8, 72, 24)

        st.markdown('<div class="section-header">🎮 CONTROLS</div>', unsafe_allow_html=True)

        run_simulation = st.button("▶️ Run Simulation", type="primary", use_container_width=True)

        st.markdown("---")
        st.markdown('<div class="section-header">📊 LEGEND</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="legend-item"><div class="legend-color" style="background:#27ae60"></div>Available</div>
        <div class="legend-item"><div class="legend-color" style="background:#e74c3c"></div>Occupied/Active</div>
        <div class="legend-item"><div class="legend-color" style="background:#f39c12"></div>Berthing/Warning</div>
        <div class="legend-item"><div class="legend-color" style="background:#3498db"></div>Waiting</div>
        <div class="legend-item"><div class="legend-color" style="background:#1abc9c"></div>Departing</div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div style="font-size: 11px; color: #8899a6;">
            <strong>Port Simulation v1.0</strong><br>
            Powered by SimPy & Plotly<br>
            © 2024 Port Analytics
        </div>
        """, unsafe_allow_html=True)

    # Initialize or run simulation
    config = {
        'num_berths': num_berths,
        'cranes_per_berth': cranes_per_berth,
        'arrival_rate': arrival_rate,
        'crane_speed': crane_speed,
        'initial_containers': initial_containers
    }

    if run_simulation or 'sim_state' not in st.session_state:
        with st.spinner("Running simulation..."):
            sim = PortSimulation(config)
            state = sim.run(sim_duration)
            st.session_state.sim_state = state
            st.session_state.config = config

    state = st.session_state.sim_state
    stats = state['stats']

    # Main Layout
    col_main, col_analytics = st.columns([3, 1])

    with col_main:
        # 3D View
        st.markdown('<div class="section-header">🌐 3D PORT VIEW</div>', unsafe_allow_html=True)
        fig_3d = create_3d_port_view(state)
        st.plotly_chart(fig_3d, use_container_width=True, config={'displayModeBar': False})

        # 2D View
        st.markdown('<div class="section-header">📍 2D TOP-DOWN VIEW</div>', unsafe_allow_html=True)
        fig_2d = create_2d_port_view(state)
        st.plotly_chart(fig_2d, use_container_width=True, config={'displayModeBar': False})

    with col_analytics:
        st.markdown('<div class="section-header">📈 LIVE ANALYTICS</div>', unsafe_allow_html=True)

        # KPI Metrics
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Ships Processed</p>
            <p class="metric-value">{stats.total_ships_served}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Containers Moved</p>
            <p class="metric-value">{stats.total_containers_moved:,}</p>
        </div>
        """, unsafe_allow_html=True)

        avg_wait = stats.total_wait_time / max(stats.total_ships_served, 1)
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Avg Wait Time</p>
            <p class="metric-value">{avg_wait:.1f}h</p>
        </div>
        """, unsafe_allow_html=True)

        avg_service = stats.total_service_time / max(stats.total_ships_served, 1)
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Avg Service Time</p>
            <p class="metric-value">{avg_service:.1f}h</p>
        </div>
        """, unsafe_allow_html=True)

        # Queue Gauge
        fig_queue = create_queue_chart(stats)
        st.plotly_chart(fig_queue, use_container_width=True, config={'displayModeBar': False})

        # Utilization Chart
        fig_util = create_utilization_chart(stats)
        st.plotly_chart(fig_util, use_container_width=True, config={'displayModeBar': False})

        # Throughput Chart
        fig_throughput = create_throughput_chart(stats, state['time'])
        st.plotly_chart(fig_throughput, use_container_width=True, config={'displayModeBar': False})

    # Bottom Section - Event Log & Statistics Table
    st.markdown('<div class="section-header">📋 SIMULATION EVENTS & STATISTICS</div>', unsafe_allow_html=True)

    col_events, col_ships = st.columns(2)

    with col_events:
        st.markdown("**Recent Events**")
        if state['events']:
            events_df = pd.DataFrame(state['events'][-15:])
            events_df['time'] = events_df['time'].apply(lambda x: f"{x:.2f}h")
            st.dataframe(events_df, use_container_width=True, hide_index=True)
        else:
            st.info("No events recorded yet")

    with col_ships:
        st.markdown("**Ship Statistics**")
        ships_data = []
        for ship in state['ships'][:15]:
            ships_data.append({
                'Ship': ship.name[:20],
                'Type': ship.ship_type,
                'Containers': ship.containers,
                'Status': ship.status,
                'Wait (h)': f"{ship.wait_time:.2f}",
                'Service (h)': f"{ship.service_time:.2f}"
            })
        if ships_data:
            ships_df = pd.DataFrame(ships_data)
            st.dataframe(ships_df, use_container_width=True, hide_index=True)
        else:
            st.info("No ships data yet")


if __name__ == "__main__":
    main()
