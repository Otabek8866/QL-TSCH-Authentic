import sys
INPUT_FILE = sys.argv[1]

delays = {}
pkt_sent = {}
pkt_received = {}
covergence_time_list = []


def main():
    total_sent_packets = 0
    with open(INPUT_FILE, "r") as f:
        for line in f:
            if not (("INFO: App" in line) and ("Sent_to" in line or "Received_from" in line)):
                continue
            if "Sent_to" in line:
                fields = line.split()

                if fields[-1] == '1':
                    covergence_time_list.append(fields)

                node_id = int(fields[1][3:])
                if node_id in pkt_sent:
                    pkt_sent[node_id][int(fields[-1])] = float(fields[0])
                else:
                    pkt_sent[node_id] = {}
                    pkt_sent[node_id][int(fields[-1])] = float(fields[0])
            elif "Received_from" in line:
                fields = line.split()
                node_id = int(fields[6])
                if node_id in pkt_received:
                    pkt_received[node_id][int(fields[-1])] = float(fields[0])
                else:
                    pkt_received[node_id] = {}
                    pkt_received[node_id][int(fields[-1])] = float(fields[0])
            else:
                print("Error: line not recognized")

    for node_id in pkt_sent.keys():
        total_sent_packets += len(pkt_sent[node_id])
        if node_id in pkt_received:
            pkt_id_list = sorted(set(pkt_sent[node_id].keys()) & set(
                pkt_received[node_id].keys()))
            not_received = sorted(
                set(pkt_sent[node_id].keys()) - set(pkt_received[node_id].keys()))
            pdr = float(len(pkt_received[node_id]))/len(pkt_sent[node_id])*100
            dels = []
            for pkt_id in pkt_id_list:
                dels.append(pkt_received[node_id]
                            [pkt_id] - pkt_sent[node_id][pkt_id])
            delays[node_id] = (dels, not_received, pdr)

        else:
            delays[node_id] = ([], sorted(pkt_sent[node_id].keys()), 0.0)

    total_time = 0
    counter = 0
    average_pdr = 0
    for i in delays.keys():
        total_time += sum(delays[i][0])
        counter += len(delays[i][0])
        average_pdr += delays[i][2]
    average_pdr = average_pdr/len(delays.keys())

    covergence_time_list.sort(reverse=True, key=lambda x: int(x[0]))

    print("\n*********** Statistics for Network *************")
    print("Average Delay: {:.2f} ms".format(total_time/counter))
    print("Packet Delivery Ratio: {:.2f}%".format(average_pdr))
    print("Total Sent Packets: {}".format(total_sent_packets))
    print("Network Convergence: {:.2f} minutes".format(float(
        int(covergence_time_list[0][0])/1000)/60))

    print("\n********* Average Delays for each Node *********")
    for i in sorted(delays.keys()):
        if len(delays[i][0]) != 0:
            print("Node {}: {:.2f} ms".format(
                i, sum(delays[i][0])/len(delays[i][0])))
        else:
            print("Node {}: No packet received -> No Delay".format(i))
        print("Packet IDs not received: {}".format(delays[i][1]))
        print("Packet Delivery Ratio: {:.2f}%".format(delays[i][2]))
        print('-' * 50)


if __name__ == "__main__":
    main()
