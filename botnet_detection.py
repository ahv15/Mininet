import numpy as np
from netml.ndm.iforest import IF
from netml.pparser.parser import PCAP
from sklearn.model_selection import train_test_split
from netml.ndm.model import MODEL
from netml.utils.tool import dump_data, load_data

pcap = PCAP(
    "D:\\BotnetDetection\\isot_app_and_botnet_dataset\\application_data\\dns_application_2017.pcap",
    flow_ptks_thres=2,
    random_state=42,
    verbose=10,
)

pcap1 = PCAP(
    "D:\\BotnetDetection\\isot_app_and_botnet_dataset\\botnet_data\\init6.pcap",
    flow_ptks_thres=2,
    random_state=42,
    verbose=10,
)


pcap.pcap2flows(q_interval=0.9)
pcap.flow2features('IAT', fft=False, header=False)
pcap1.pcap2flows(q_interval=0.9)
pcap1.flow2features('IAT', fft=False, header=False)
dump_data((pcap.features, pcap.labels), out_file='out/IAT-features.dat')
dump_data((pcap1.features, pcap1.labels), out_file='out/IAT-features1.dat')
(features, labels) = load_data('out/IAT-features.dat')
(features1, labels1) = load_data('out/IAT-features1.dat')
final_features = np.vstack([features, features1])
final_labels = []
for i in range(len(features)):
    final_labels.append(0)
for i in range(len(features1)):
    final_labels.append(1)
(features_train, features_test, labels_train, labels_test) = train_test_split(final_features, final_labels, test_size= 0.33, random_state=42, shuffle=True)
model = IF(n_estimators=100, random_state=42)
model.name = 'IF'
ndm = MODEL(model, score_metric='auc', verbose=10, random_state=42)
ndm.train(features_train)
ndm.test(features_test, labels_test)
print(pcap.features.shape, pcap.pcap2flows.tot_time, pcap.flow2features.tot_time)
print(ndm.train.tot_time, ndm.test.tot_time, ndm.score)