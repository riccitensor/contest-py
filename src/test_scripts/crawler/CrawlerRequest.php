<?php
/**
 * Created by IntelliJ IDEA.
 * User: de
 * Date: 10/17/11
 * Time: 3:30 PM
 *
 * bridges request to python server and returns an
 * object with (url, content, dateCreated) fields.
 *
 * usage: $detailData = new CrawlerRequest("http://www.example.com/article/123.html");
 */
 
class CrawlerRequest {
    protected $crawlerBaseUrl = "http://127.0.0.1:5000/test/crawl/url?url=";

    function doRequest($url) {
        $crawlUrl = $this->crawlerBaseUrl . $url;
        $jsonData = false;
        try {
            if (! $jsonData = file_get_contents($crawlUrl,0,null,null) )
                return false;
        }
        catch(Exception $e) {
            cb_log("CrawlerServer:work(): " . $e->getMessage(), 'error');
            return false;
        }
        return json_decode($jsonData);
    }
	
	/*
     * checks redis for full text and returns it
     * if nothing is found then a new job to get fulltext is created
     * returns itemDetails Object or false
     * todo: make protected (public for testing purpose)
     */
	/* example for querying
	$itemDetails = $this->getItemDetails($item);
	if ($itemDetails) {
		$item->title        = $itemDetails->title;
		$item->content      = $itemDetails->content;
		$item->dateCreated  = $itemDetails->dateCreated;
	}*/
    public function getItemDetails($item) {
		$redis = ClickabillyRedis::getInstance();
		
        //detail information for this item in redis?
        $itemDetails = $redis->get("clickabilly:item:details:$item->id");
        if ($itemDetails) {
            return unserialize($itemDetails);
        }
        else {
            $crawlJob = new stdClass();
            $crawlJob->url=$item->url;
            $crawlJob->id =$item->id;

            //save new job for worker in sorted set. if it exits the score will be increased by 1
            $redis->zincrby("clickabilly:crawler:jobs",1,serialize($crawlJob));
        }
        return false;
    }
}