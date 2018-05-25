<?php

namespace App\Http\Controllers;

use App\Patent;
use GuzzleHttp\Client;
use GuzzleHttp\RequestOptions;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;
use Ramsey\Uuid\Uuid;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

class CnkiController
{

    public function upload(Request $request)
    {
        $file = $request->file('file');
        $content = file_get_contents($file->getRealPath());
        $api = config("app.nlp_api");
        $client = new Client();
        $res = $client->post($api, [
            RequestOptions::JSON => ['content' => $content]
        ]);
        $result = (string)$res->getBody();
        $uuid = Uuid::uuid4()->toString();
        Cache::add($uuid, $result, 120);

        $response = [
            "result" => $uuid
        ];

        return $response;
    }

    public function result($uuid)
    {
        $result = Cache::get($uuid);
        if (!isset($result)) {
            throw new NotFoundHttpException();
        }
        $result = json_decode($result, true);
        $patent2Similarity = [];
        $patentIds = [];
        foreach ($result as $r) {
            $patentId = $r['id'];
            $patent2Similarity[$patentId] = $r['ratio'];
            $patentIds[] = $patentId;
        }
        $patents = Patent::find($patentIds);
        $datas = [];
        foreach ($patents as $p) {
            $sr = round($patent2Similarity[$p->id] * 100, 2) . '%';
            $d = [
                'id' => $p->id,
                'original_name' => $p->original_name,
                'patent_name' => $p->patent_name,
                'abstract' => $p->internalStage->abstract,
                'similar_rate' => $sr
            ];
            $datas[] = $d;
        }
        return $datas;
    }

}