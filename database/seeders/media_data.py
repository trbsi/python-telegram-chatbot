from pathlib import Path

media_list = [
    {
        "file_id": "4_zcfd254da56d763b1999f0b1d_f1065d6c71546b69a_d20250927_m104423_c005_v0501036_t0052_u01758969863111",
        "bucket_id": "cfd254da56d763b1999f0b1d",
        "file_path": "inbox_2503_b39029e9-6280-4ca9-a820-f69426015d3a.jpg",
        "bucket_name": "swyveltd"
    },
    {
        "file_id": "4_zcfd254da56d763b1999f0b1d_f1092bf377f83edab_d20250927_m104641_c005_v0501002_t0029_u01758970001064",
        "bucket_id": "cfd254da56d763b1999f0b1d",
        "file_path": "inbox_2504_aa67c1ad-9ee1-4ca4-87f1-3df30ea12a92.mp4",
        "bucket_name": "swyveltd"
    },
    {
        "file_id": "4_zcfd254da56d763b1999f0b1d_f102895e580648cfe_d20250927_m105024_c005_v0501039_t0058_u01758970224077",
        "bucket_id": "cfd254da56d763b1999f0b1d",
        "file_path": "inbox_2505_fc327982-6e1a-48af-9c5b-fbb5904aeeed.jpg",
        "bucket_name": "swyveltd"
    },
    {
        "file_id": "4_zcfd254da56d763b1999f0b1d_f101f2838642f2e99_d20250927_m105049_c005_v0501039_t0054_u01758970249736",
        "bucket_id": "cfd254da56d763b1999f0b1d",
        "file_path": "inbox_2506_d28e1e21-16b4-44c2-afda-9ea0f5659707.jpg",
        "bucket_name": "swyveltd"
    },
    {
        "file_id": "4_zcfd254da56d763b1999f0b1d_f105b3711c926c45e_d20250927_m105119_c005_v0501010_t0032_u01758970279343",
        "bucket_id": "cfd254da56d763b1999f0b1d",
        "file_path": "inbox_2507_d1aa7e66-3d2f-496f-8400-5ed4317c82f5.jpg",
        "bucket_name": "swyveltd"
    },
    {
        "file_id": "4_zcfd254da56d763b1999f0b1d_f1142c8684f0eeaac_d20250927_m105203_c005_v0501007_t0044_u01758970323136",
        "bucket_id": "cfd254da56d763b1999f0b1d",
        "file_path": "inbox_2508_a4ccce01-f747-4300-af95-5c1bbaabd2ea.mp4",
        "bucket_name": "swyveltd"
    },
    {
        "file_id": "4_zcfd254da56d763b1999f0b1d_f105332e50fd85168_d20250927_m105245_c005_v0501034_t0047_u01758970365043",
        "bucket_id": "cfd254da56d763b1999f0b1d",
        "file_path": "inbox_2509_0b0d566b-7cb0-484d-99aa-a4a785795780.mp4",
        "bucket_name": "swyveltd"
    },
    {
        "file_id": "4_zcfd254da56d763b1999f0b1d_f10452d0ac2872cde_d20250927_m105302_c005_v0501031_t0055_u01758970382233",
        "bucket_id": "cfd254da56d763b1999f0b1d",
        "file_path": "inbox_2510_38d20542-399f-4437-8bdb-4f34c24e6db4.mp4",
        "bucket_name": "swyveltd"
    },
    {
        "file_id": "4_zcfd254da56d763b1999f0b1d_f10037cce51ab3fdc_d20250927_m105327_c005_v0501037_t0041_u01758970407664",
        "bucket_id": "cfd254da56d763b1999f0b1d",
        "file_path": "inbox_2511_e522f388-957f-482a-ace0-7cbd3e232213.mp4",
        "bucket_name": "swyveltd"
    }
]

thumbnail_list = []
for media in media_list:
    extension = Path(media['file_path']).suffix
    if extension == '.jpg':
        thumbnail_list.append(media)
