<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Aurexus Dashboard</title>
    <!-- ================= Favicon ================== -->
    <!-- Standard -->
    <!--<link href="assets/css/lib/calendar2/pignose.calendar.min.css" rel="stylesheet">-->
    <link href="assets/css/lib/chartist/chartist.min.css" rel="stylesheet">
    <link href="assets/css/lib/font-awesome.min.css" rel="stylesheet">
    <link href="assets/css/lib/themify-icons.css" rel="stylesheet">
    <!--<link href="assets/css/lib/owl.carousel.min.css" rel="stylesheet" />
    <link href="assets/css/lib/owl.theme.default.min.css" rel="stylesheet" />
    <link href="assets/css/lib/weather-icons.css" rel="stylesheet" />-->
    <link href="assets/css/lib/menubar/sidebar.css" rel="stylesheet">
    <link href="assets/css/lib/bootstrap.min.css" rel="stylesheet">
    <link href="assets/css/lib/helper.css" rel="stylesheet">
    <link href="assets/css/style.css" rel="stylesheet">
<style>
.dot {
  height: 10px;
  width: 10px;
  border-radius: 50%;
  display: inline-block;
}
.progresscircle{
    width: 150px;
    height: 150px;
    line-height: 150px;
    background: none;
    margin: 0 auto;
    box-shadow: none;
    position: relative;
}
.progresscircle:after{
    content: "";
    width: 100%;
    height: 100%;
    border-radius: 50%;
    border: 12px solid #fff;
    position: absolute;
    top: 0;
    left: 0;
}
.progresscircle > span{
    width: 50%;
    height: 100%;
    overflow: hidden;
    position: absolute;
    top: 0;
    z-index: 1;
}
.progresscircle .progresscircle-left{
    left: 0;
}
.progresscircle .progresscircle-bar{
    width: 100%;
    height: 100%;
    background: none;
    border-width: 12px;
    border-style: solid;
    position: absolute;
    top: 0;
}
.progresscircle .progresscircle-left .progresscircle-bar{
    left: 100%;
    border-top-right-radius: 80px;
    border-bottom-right-radius: 80px;
    border-left: 0;
    -webkit-transform-origin: center left;
    transform-origin: center left;
}
.progresscircle .progresscircle-right{
    right: 0;
}
.progresscircle .progresscircle-right .progresscircle-bar{
    left: -100%;
    border-top-left-radius: 80px;
    border-bottom-left-radius: 80px;
    border-right: 0;
    -webkit-transform-origin: center right;
    transform-origin: center right;
    animation: loading-1 1.8s linear forwards;
}
.progresscircle .progresscircle-value{
    width: 90%;
    height: 90%;
    border-radius: 50%;
    background: #44484b;
    font-size: 24px;
    color: #fff;
    line-height: 135px;
    text-align: center;
    position: absolute;
    top: 5%;
    left: 5%;
}
.progresscircle.blue .progresscircle-bar{
    border-color: #049dff;
}
.progresscircle.blue .progresscircle-left .progresscircle-bar{
    animation: loading-2 1.5s linear forwards 1.8s;
}
 
 .progresscircle-left .progresscircle-bar{
    animation: loading-3 1s linear forwards 1.8s;
}

 .progresscircle-left .progresscircle-bar{
    animation: loading-4 0.4s linear forwards 1.8s;
}

 .progresscircle-left .progresscircle-bar{
    animation: loading-5 1.2s linear forwards 1.8s;
}

@keyframes loadings-1 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(180deg);
    transform: rotate(180deg);
  }
}
@keyframes loadings-2 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(144deg);
    transform: rotate(144deg);
  }
}
@keyframes loadings-3 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(135deg);
    transform: rotate(135deg);
  }
}
@keyframes loading-1{
    0%{
        -webkit-transform: rotate(0deg);
        transform: rotate(0deg);
    }
    100%{
        -webkit-transform: rotate(180deg);
        transform: rotate(180deg);
    }
}
@keyframes loading-2{
    0%{
        -webkit-transform: rotate(0deg);
        transform: rotate(0deg);
    }
    100%{
        -webkit-transform: rotate(180deg);
        transform: rotate(180deg);
    }
}
@keyframes loading-3{
    0%{
        -webkit-transform: rotate(0deg);
        transform: rotate(0deg);
    }
    100%{
        -webkit-transform: rotate(90deg);
        transform: rotate(90deg);
    }
}
@keyframes loading-4{
    0%{
        -webkit-transform: rotate(0deg);
        transform: rotate(0deg);
    }
    100%{
        -webkit-transform: rotate(180deg);
        transform: rotate(180deg);
    }
}
@media only screen and (max-width: 990px){
    .progresscircle{ margin-bottom: 20px; }
}

.gauge {
  width: 100%;
 /* max-width: 250px;*/
  font-family: "Roboto", sans-serif;
  font-size: 32px;
  color: #004033;
}

.gauge__body {
  width: 100%;
  height: 0;
  padding-bottom: 50%;
  background: #e7e7e7;
  position: relative;
  border-top-left-radius: 100% 200%;
  border-top-right-radius: 100% 200%;
  overflow: hidden;
}

.gauge__fill {
  position: absolute;
  top: 100%;
  left: 0;
  width: inherit;
  height: 100%;
  background: #005CE1;
  transform-origin: center top;
  transform: rotate(0.25turn);
  transition: transform 0.2s ease-out;
}

.gauge__cover {
  width: 75%;
  height: 150%;
  background: #ffffff;
  border-radius: 50%;
  position: absolute;
  top: 25%;
  left: 50%;
  transform: translateX(-50%);

  /* Text */
  display: flex;
  align-items: center;
  justify-content: center;
  padding-bottom: 25%;
  box-sizing: border-box;
  color:#265fde;
}
.sidebar> .nano> .nano-content{
    width:10px;
}

</style>
</head>
<body>
        <div class="sidebar sidebar-hide-to-small sidebar-shrink sidebar-gestures">
        <div class="nano">
            <div class="nano-content">
                    <?php include('navigation.php')?>
                    
            </div>
        </div>
    </div>
    <!-- /# sidebar -->

    <div class="header">
        <div class="container-fluid">
            <div class="row">
                <div class="col-lg-12">
                    <div class="float-left">
                        <div class="hamburger sidebar-toggle">
                            <span class="line"></span>
                            <span class="line"></span>
                            <span class="line"></span>
                        </div>
                    </div>
                    <div class="float-left">
                            <div class="">
                                <ol class="breadcrumb">
                                    <li class="breadcrumb-item"><a href="#">Dashboard</a></li>
                                    <li class="breadcrumb-item active">Home</li>
                                </ol>
                            </div>
                    </div>
                    <div class="float-left">
                        <div class="">
                                <ol class="breadcrumb">
                                    <li class="breadcrumb-item"><a class='badge badge-warning'><b>PROJECT CAEN</b></a></li>
                                </ol>
                            </div>
                         
                    </div>
                    <div class="float-right">
                        <div class="header-icon" disabled="disabled">
                            <img  width="90px" height="30px" src="https://www.aurexus.com/wp-content/uploads/2021/10/1_80x50mm_adobe_illustratorwhite.png"></img>
                        </div>
                        <div class="header-icon">
                            
                            <button class="btn btn-primary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                             <img class="form-control-sm" src="./us_flag.png">English
                            </button>
                             <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                <a class="dropdown-item" href="https://aurexusmedusa.azurewebsites.net/MedusaV3_1/fr/home.php"><img class="form-control-sm" src="./fr_flag.png">French</a>
                             </div>
                        </div>                       
                        
                        <div class="dropdown dib">
                            <div class="header-icon" data-toggle="dropdown">
                                <span class="user-avatar"><?php echo $usernme;?>
                                    <i class="ti-angle-down f-s-10"></i>
                                </span>
                                <div class="drop-down dropdown-profile dropdown-menu dropdown-menu-right">
                                    
                                    <div class="dropdown-content-body">
                                        <ul>                                            
                                            <li>
                                            <a href='index.php' target='_blank'>
                                                <i class="ti-file"></i> Documentation</a>
                                            </li>
                                            <li>
                                            <a href='index.php' onclick="myclickFunction()">
                                                <i class="ti-power-off"></i> Logout</a>
                                            </li>
                                            
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <div class="content-wrap">
        <div class="main">
            <div class="container-fluid">
                
                <!-- /# row -->
                <section id="main-content">
                    <div class="row">
                        <div class="col-lg-4">
                             <div class="card nestable-cart">
                                <div class="card-title">
                                    <h4>Project Quantity</h4>
                                </div><br/>
                                    <!-- python code -->
                      <div class="d-flex justify-content-center padding">
                            <div class="row">
                                <div class="col-md-12 col-sm-6">
                                     <div class="progresscircle blue">
                                        <span class="progresscircle-left">
                                        <span class="progresscircle-bar"></span>
                                        </span>
                                        <span class="progresscircle-right">
                                        <span class="progresscircle-bar"></span>
                                        </span>
                                            <div class="progresscircle-value"><?php echo $quant?></div>
                                    </div>
                                </div>
                                <div class="col-md-12 col-sm-6 text-center"><h5>Notices</h5></div>
                            </div>
                      </div>                          
                    
                  <!-- /# column -->
                </div>
                           
                            <div class="card">
                                <div class="card-title">
                                    <h4>Total Notice Per Traitement </h4>
                                </div>
                                <div class="card-body">
                                    <div class="table-responsive">
                                         <table class="table table-striped">
                                            <thead>
                                                <tr>
                                                    <th>Traitements</th>
                                                    <th>Quantity</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                            <!--python code -->
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                            <!-- /# card -->
                        </div>
                        <div class="col-lg-4">
                                   <div class="card">
                                      <div class="card-title">
                                         <h4>Overall Project Progress </h4>
                                      </div>
                                          <div class="justify-content-center padding">
                                <div class="row">
                                <div class="col-md-12 col-sm-12 text-center">
                                <div class="gauge">
                                    <div class="gauge__body">
                                        <div class="gauge__fill"></div>
                                        <div class="gauge__cover"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>    
                        <div class="row">
                                <div class="col-md-12 text-center"><span class="dot" style="background-color: #005CE1;"></span> % project completed
                                <span class="dot" style="background-color: #E7E7E7;"></span> % project yet to be completed</div>
                            </div>
                                   </div>
                                   <div class="card">
                                      <div class="card-title">
                                         <h4>Stage Progress  <a href="#" target="_blank" type="button" class="btn-sm btn-primary btn-flat" title="Link">Report</a></h4>
                                      </div><br/>
                                              <!-- python code -->
                                   </div>
                        </div>
                        <div class="col-md-4">
                          <div class="card">
                                <div class="card-title">
                                    <h4>Anomalie Progress </h4>
                                    <div class="panel">
                                        <div class="panel-body">
                                            <canvas id="myChart" style="display: block; height: 218px; width: 288px;"></canvas>
                                        </div>
                                    </div>
                                </div>
                                <div class="card-body">
                                </div>
                          </div>
                          <div class="card" style="height: 518px !important;overflow: scroll;">
                                <div class="card-title">
                                    <h4>Total Anomalie To Process</h4>
                                </div>
                                <div class="card-body">
                                     <table class="table table-striped">
                                            <thead>
                                                <tr>
                                                    <th>Folders</th>
                                                    <th></th>
                                                    <th>Total Ano</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <!-- python code -->
                                            </tbody>
                                        </table>
                                </div>
                          </div>  
                       </div>
                    </div>
                    <!-- /# row -->
                    
                    <!-- /# row -->
                    <div class="row">
                        <div class="col-lg-12">
                            <div class="footer">
                                <p>© Aurexus. - <a href="http://aurexus.com">aurexus.com</a></p>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    </div>

    <!-- jquery vendor -->
    <script src="assets/js/lib/jquery.min.js"></script>
    <script src="assets/js/lib/jquery.nanoscroller.min.js"></script>
    <!-- nano scroller -->
    <script src="assets/js/lib/menubar/sidebar.js"></script>
    <script src="assets/js/lib/preloader/pace.min.js"></script>
    <!-- sidebar -->

    <script src="assets/js/lib/bootstrap.min.js"></script>
    <script src="assets/js/scripts.js"></script>
    <!-- bootstrap -->

    <script src="assets/js/lib/calendar-2/moment.latest.min.js"></script>
    <script src="assets/js/lib/calendar-2/pignose.calendar.min.js"></script>
    <script src="assets/js/lib/calendar-2/pignose.init.js"></script>
    <script src="assets/js/lib/peitychart/jquery.peity.min.js"></script>
    <script src="assets/js/lib/peitychart/peitychart.init.js"></script>
    <script src="assets/js/lib/knob/jquery.knob.min.js "></script>
    <script src="assets/js/lib/knob/knob.init.js "></script>
    <script src="assets/js/lib/chart-js/Chart.bundle.js"></script>
    <script src="assets/js/lib/chart-js/chartjs-init.js"></script>


    <!--<script src="assets/js/lib/weather/jquery.simpleWeather.min.js"></script>
    <script src="assets/js/lib/weather/weather-init.js"></script>-->
    <script src="assets/js/lib/circle-progress/circle-progress.min.js"></script>
    <script src="assets/js/lib/circle-progress/circle-progress-init.js"></script>
    <script src="assets/js/lib/chartist/chartist.min.js"></script>
    <script src="assets/js/lib/sparklinechart/jquery.sparkline.min.js"></script>
    <script src="assets/js/lib/sparklinechart/sparkline.init.js"></script>
    <!--<script src="assets/js/lib/owl-carousel/owl.carousel.min.js"></script>
    <script src="assets/js/lib/owl-carousel/owl.carousel-init.js"></script>-->
    <!-- scripit init-->
    <script>
    
const ctx = document.getElementById('myChart');
var todo= "<?php echo $todo; ?>";
var done= "<?php echo $done; ?>";
var percent="<?php echo ($donutchart/100);?>";
const myChart = new Chart(ctx,{
    type: 'doughnut',
    data: {
        labels: ['Done('+done+')','To Do('+todo+')'],
        datasets: [{
            data: [done, todo],
            backgroundColor: [
                'rgba(97, 100, 193)',
                'rgba(231, 231, 231)'
            ],
            borderWidth: 1
        }]
    },
   options: {
      title: {
        display: true,
        text: '',
        position:'bottom'
      }
    },plugins: {
    datalabels: true
  }
    
});

const gaugeElement = document.querySelector(".gauge");

function setGaugeValue(gauge, value) {
  if (value < 0 || value > 1) {
    return;
  }

  gauge.querySelector(".gauge__fill").style.transform = `rotate(${
    value / 2
  }turn)`;
  gauge.querySelector(".gauge__cover").textContent = `${Math.round(
    value * 100
  )}%`;
}

setGaugeValue(gaugeElement, percent);
</script>
<script>
function myclickFunction(){
        window.location.href="index.php";
    }
</script>
<script src="assets/js/dashboard2.js"></script>
</body>

</html>