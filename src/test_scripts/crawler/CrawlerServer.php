<?php
/**
 * Created by IntelliJ IDEA.
 * User: de
 * Date: 10/11/11
 * Time: 4:53 PM
 * To change this template use File | Settings | File Templates.
 */
 
class CrawlerServer {

    // how to reach the crawler
    private $crawlerBaseUrl = "http://127.0.0.1:5000/test/crawl/url?url=";

    // redis instance
	private $redis;

    // this child process id
    private $processid;

    // seconds that a child may do nothing until it is hanging
    private $secondsToZombieChild = 120;

	function __construct() {
		$this->redis = ClickabillyRedis::getInstance();
	}

    /*
     * forks a CrawlerServer child if not already $childWorkerCount Processes are running
     */
	public function run($childWorkerCount=1) {

        //count current started and running workers
        $startedWorkerCount = count($this->redis->keys("clickabilly:crawler:worker:started*"));
        $runningWorkerCount = count($this->redis->keys("clickabilly:crawler:worker:running*"));

        /*
         * kill zombie processes
         */
        if ($startedWorkerCount > $runningWorkerCount) {
            $this->cleanZombieProcesses();
        }

        /*
         * we have to fork
         */
        if ($runningWorkerCount <= $childWorkerCount) {
            $pid = pcntl_fork();
            if ($pid == -1) {
                cb_log("CrawlerServer:run(): Could not fork", 'error');
            } else if ($pid) {

                // This is the parent process go on to handle the request
                cb_log("Started process (PID $pid)");
                $this->redis->set("clickabilly:crawler:worker:started:$pid","1");

            } else {

                // This is the child process (actual worker)
                $this->processid = getmypid();

                // mark process running and started in redis
                $this->redis->setex("clickabilly:crawler:worker:running:$this->processid",$this->secondsToZombieChild,"1");

                $this->work();
            }
        }
        return;
    }

    protected function work() {
        while (1) {

            // set worker alive for x seconds (afterwards it is seen as if it is dead)
            $secondsUntilExpire=60;
            $this->redis->setex("clickabilly:crawler:worker:running:$this->processid",$this->secondsToZombieChild,"1");


            //select job with maximum score
            $workItem = $this->redis->zRevRange("clickabilly:crawler:jobs",0,0);

            if ($workItem) {

                //get first element in multi bulk reply from zrevrange
                foreach($workItem as $item) { $workItem = $item; }

                //remove job from list
                $this->redis->zRem("clickabilly:crawler:jobs", $workItem);

                //decode data
                $workItem = unserialize($workItem);

                /*
                 * ask crawler server to get itemDetails
                 */
                if ($workItem->id && $workItem->url)
                {
                    /*
                     * call the crawler to get details
                     */
                    cb_log("CrawlerServer:work(): getting contents for item id: " .
                            $workItem->id . " with url " . $workItem->url);

                    $crawlUrl = $this->crawlerBaseUrl . $workItem->url;
                    $jsonData = false;
                    try {
                        if (! $jsonData = file_get_contents($crawlUrl,0,null,null) )
                            throw new Exception('Load Failed: '. $crawlUrl);
                    }
                    catch(Exception $e) {
                        cb_log("CrawlerServer:work(): " . $e->getMessage(), 'error');
                    }

                    /*
                     * save the result
                     */
                    if ($jsonData) {
                        $itemDetail = json_decode($jsonData);
                        $this->redis->set("clickabilly:item:details:$workItem->id",serialize($itemDetail));
                    }
                }
                else
                {
                    cb_log("CrawlerServer:work(): illegal job arguments");
                }
            }
            /*
             * there was nothing to do: sleep
             */
            else {
                sleep(10);
            }
        }
    }

    /*
     * kills all processes that are started and not working currently
     */
    protected function cleanZombieProcesses() {

        /*
         * get array of started and running pids
         */
        $runningWorkersList = array();
        $startedWorkersList = array();

        $runningWorkers = $this->redis->keys("clickabilly:crawler:worker:running*");
        $startedWorkers = $this->redis->keys("clickabilly:crawler:worker:started*");

        foreach($runningWorkers as $item) { $runningWorkers = explode(":",$item); $runningWorkersList[] += $runningWorkers[4]; }
        foreach($startedWorkers as $item) { $startedWorkers = explode(":",$item); $startedWorkersList[] += $startedWorkers[4]; }

        /*
         * kill pids that are started but not running
         */
        foreach($startedWorkersList as $startedProcessId) {
            if (! in_array($startedProcessId,$runningWorkersList) && $startedProcessId > 0) {
                cb_log("CrawlerServer:cleanZombieProcesses(): shutting down pid ". $startedProcessId);
                posix_kill($startedProcessId, 9);
                $this->redis->del("clickabilly:crawler:worker:started:$startedProcessId");
            }
        }
    }

    public function stopAllProcesses() {
        $runningWorkers = $this->redis->keys("clickabilly:crawler:worker:running*");
        foreach($runningWorkers as $item) {
            $runningWorkers = explode(":",$item);
            $pid = $runningWorkers[4];
            posix_kill($pid, 9);
            $this->redis->del("clickabilly:crawler:worker:running:$pid");
        }

        $startedWorkers = $this->redis->keys("clickabilly:crawler:worker:started*");
        foreach($startedWorkers as $item) {
            $startedWorkers = explode(":",$item);
            $pid = $startedWorkers[4];
            posix_kill($pid, 9);
            $this->redis->del("clickabilly:crawler:worker:started:$pid");
        }
    }

}
